from setuptools import find_packages, setup

package_name = "pui89_sim_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="PUI89 AI Robotics",
    maintainer_email="puinuanmanee@gmail.com",
    description="Simulation-only ROS 2 symbolic proposal bridge. No actuator commands.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "pui89_sim_proposal_bridge = pui89_sim_bridge.proposal_node:main",
        ],
    },
)
