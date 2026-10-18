from __future__ import annotations

from dataclasses import dataclass

import torch

from coconut_harvest_robot.action_model import AdvancedActionModel
from coconut_harvest_robot.config import RobotConfig
from coconut_harvest_robot.data import SyntheticOrchard
from coconut_harvest_robot.kinematic_solver import TrajectoryPlanner, KinematicSolver
from coconut_harvest_robot.spatial import SpatialFeatureExtractor
from coconut_harvest_robot.vision import TreeVisionEncoder


@dataclass
class HarvestResult:
    scene_repr: torch.Tensor
    spatial_features: torch.Tensor
    action_logits: torch.Tensor
    action_plan: dict
    harvest_pose: dict
    trajectory_waypoints: list[dict]

    def summary(self) -> str:
        return (
            f"scene={tuple(self.scene_repr.shape)}, "
            f"spatial={tuple(self.spatial_features.shape)}, "
            f"action={tuple(self.action_logits.shape)}, "
            f"waypoints={len(self.trajectory_waypoints)}"
        )


class HarvestPipeline:
    def __init__(self, config: RobotConfig | None = None):
        self.config = config or RobotConfig()
        self.vision_encoder = TreeVisionEncoder(out_dim=16)
        self.spatial_extractor = SpatialFeatureExtractor(in_channels=4, out_dim=16)
        self.action_model = AdvancedActionModel(in_dim=32, action_dim=self.config.action_dim)
        self.trajectory_planner = TrajectoryPlanner(
            max_iterations=self.config.rrt_iterations,
            planning_timeout_s=self.config.planning_timeout_s,
        )
        self.kinematics_solver = KinematicSolver(dof=self.config.arm_dof)

    def tokenize_instruction(self, instruction: str) -> torch.Tensor:
        vocab = {ch: idx + 1 for idx, ch in enumerate(sorted(set(instruction.lower())))}
        tokens = [vocab.get(ch, 0) for ch in instruction.lower()]
        return torch.tensor(tokens, dtype=torch.long)

    def __call__(self, rgb: torch.Tensor, depth: torch.Tensor, instruction: str) -> HarvestResult:
        if rgb.dim() != 4:
            raise ValueError("Expected RGB tensor with shape [B, C, H, W]")
        if depth.dim() != 4:
            raise ValueError("Expected depth tensor with shape [B, C, H, W]")

        scene_repr = self.vision_encoder(rgb)
        spatial_features = self.spatial_extractor(rgb, depth)

        fused = torch.cat((scene_repr, spatial_features), dim=1)
        action_logits = self.action_model(fused)

        action_plan = {
            "task": "approach_upper_coconut",
            "status": "planned",
            "confidence": float(torch.softmax(action_logits, dim=-1).max().item()),
            "instruction": instruction,
        }

        harvest_pose = {
            "x_m": 2.1,
            "y_m": 1.4,
            "z_m": 6.8,
            "yaw_deg": 18.0,
            "gripper": "open",
        }

        # Generate trajectory
        start_pose = torch.zeros(6)
        target_pose = torch.tensor([0.5, 0.3, -0.2, 1.57, 0.0, 0.0])
        obstacle_map = torch.zeros(256, 256)

        traj_result = self.trajectory_planner(start_pose, target_pose, obstacle_map)
        trajectory_waypoints = [
            {"index": i, "pose": wp.tolist()}
            for i, wp in enumerate(traj_result["waypoints"])
        ]

        return HarvestResult(
            scene_repr=scene_repr,
            spatial_features=spatial_features,
            action_logits=action_logits,
            action_plan=action_plan,
            harvest_pose=harvest_pose,
            trajectory_waypoints=trajectory_waypoints,
        )

    def generate_demo_scene(self) -> tuple[torch.Tensor, torch.Tensor]:
        rgb = SyntheticOrchard.generate_rgb()
        depth = SyntheticOrchard.generate_depth()
        return rgb, depth
