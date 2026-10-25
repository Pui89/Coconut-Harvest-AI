"""ROS 2 node that converts simulated state JSON into symbolic proposals.

Input: /pui89/sim/world_state (std_msgs/String JSON)
Output: /pui89/sim/action_proposal (std_msgs/String JSON)

This node intentionally does not publish physical control or navigation commands.
"""
from __future__ import annotations

import json
import time

from .decision_gate import ALLOWED_READY_ACTIONS, evaluate_world_state


def main(args=None) -> None:
    # Import ROS dependencies only when the executable is actually launched.
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    class SimProposalNode(Node):
        def __init__(self) -> None:
            super().__init__("pui89_sim_proposal_bridge")
            self.declare_parameter("project_id", "pui89-simulation")
            self.declare_parameter("ready_action", "REQUEST_HUMAN_REVIEW")
            self.declare_parameter("confidence_threshold", 0.65)
            self.project_id = str(self.get_parameter("project_id").value)
            self.ready_action = str(self.get_parameter("ready_action").value)
            self.threshold = float(self.get_parameter("confidence_threshold").value)
            if self.ready_action not in ALLOWED_READY_ACTIONS:
                raise ValueError(f"ready_action must be one of {sorted(ALLOWED_READY_ACTIONS)}")
            self.publisher = self.create_publisher(String, "/pui89/sim/action_proposal", 10)
            self.subscription = self.create_subscription(
                String, "/pui89/sim/world_state", self.on_state, 10
            )
            self.get_logger().info(
                f"Simulation-only proposal bridge ready for {self.project_id}; no actuator topics enabled."
            )

        def on_state(self, message) -> None:
            out = String()
            try:
                state = json.loads(message.data)
                if not isinstance(state, dict):
                    raise ValueError("world state must be a JSON object")
                proposal = evaluate_world_state(
                    state,
                    ready_action=self.ready_action,
                    confidence_threshold=self.threshold,
                )
                proposal.update({
                    "project_id": self.project_id,
                    "observed_at_unix_s": time.time(),
                    "input_schema": "pui89.world_state.v1",
                })
                out.data = json.dumps(proposal, sort_keys=True)
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                out.data = json.dumps({
                    "schema_version": 1,
                    "project_id": self.project_id,
                    "action": "UNKNOWN",
                    "reason_codes": ["INVALID_WORLD_STATE_JSON"],
                    "error_type": type(exc).__name__,
                    "hardware_actuation": False,
                    "simulation_only": True,
                    "input_schema": "pui89.world_state.v1",
                }, sort_keys=True)
                self.get_logger().warning(f"World-state input rejected: {type(exc).__name__}")
            self.publisher.publish(out)

    rclpy.init(args=args)
    node = None
    try:
        node = SimProposalNode()
        rclpy.spin(node)
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
