import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.actions import LifecycleNode
import xacro

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default=False)

    robotXacroName        = 'kobuki'
    namePackage           = 'kobuki_description'
    modelFileRelativePath = 'model/kobuki_sim.xacro'
    worldFileRelativePath = 'worlds/playground.sdf'
    rvizFileRelativePath  = 'rviz/rviz_config.rviz'

    pathModelFile         = os.path.join(get_package_share_directory(namePackage), modelFileRelativePath)
    robotDescription      = xacro.process_file(pathModelFile).toxml()
    pathWorldFile         = os.path.join(get_package_share_directory(namePackage), worldFileRelativePath)
    pathRvizConfig        = os.path.join(get_package_share_directory(namePackage), rvizFileRelativePath)

                                                                    # --------------- GAZEBO CONFIGURATION --------------- 

    # gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'))
    # gazebo_launch           = IncludeLaunchDescription(gazebo_rosPackageLaunch, launch_arguments={'gz_args': [f'-r {pathWorldFile}'], 'on_exit_shutdown' : 'true'}.items())
    # # gazebo_launch           = IncludeLaunchDescription(gazebo_rosPackageLaunch, launch_arguments={'gz_args': ['-r empty.sdf'], 'on_exit_shutdown' : 'true'}.items())

    # spawnModelNodeGazebo  = Node(
    #     package    = 'ros_gz_sim',
    #     executable = 'create',
    #     parameters=[{'use_sim_time': use_sim_time}],
    #     arguments  = [
    #         '-name' , robotXacroName,
    #         '-topic', 'robot_description'
    #     ],
    #     output     = 'screen'
    # )

    # bridge_params = os.path.join(get_package_share_directory(namePackage), 'parameters', 'bridge_parameters.yaml')
    
    # startGazeboRosBridgeCmd = Node(
    #     package    = 'ros_gz_bridge',
    #     executable = 'parameter_bridge',
    #     arguments  = [
    #         '--ros-args',
    #         '-p',
    #         f'config_file:={bridge_params}',
    #     ],
    #     output     = 'screen'
    # )

                                                                    # --------------- RVIZ CONFIGURATION --------------- 

    spawnModelNodeRviz = Node(
        package    = 'rviz2',
        executable="rviz2",
        name="rviz2",
        output="screen",
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=["-d", pathRvizConfig],
    )

    nodeRobotStatePublisher = Node(
        package    = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output     = 'screen',
        parameters = [{
            'robot_description': robotDescription,
            'use_sim_time'     : False,
        }]
    )

    joint_state_publisher = Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher'
    )

    launchDescriptionObject = LaunchDescription()

    # launchDescriptionObject.add_action(gazebo_launch)
    
    launchDescriptionObject.add_action(nodeRobotStatePublisher)
    launchDescriptionObject.add_action(joint_state_publisher)
    # launchDescriptionObject.add_action(startGazeboRosBridgeCmd)
    launchDescriptionObject.add_action(spawnModelNodeRviz)

    return launchDescriptionObject