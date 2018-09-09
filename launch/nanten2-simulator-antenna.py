<launch>

  <node pkg = "necst_ros3"
      name = "antenna_drive"
      type = "antenna_drive.py" />

  <node pkg = "necst_ros3"
      name = "antenna_drive_sim"
      type = "antenna_drive_sim.py" />

  <node pkg = "necst_ros3"
      name = "antenna_drive_lock"
      type = "antenna_drive_lock.py" />

  <node pkg = "necst_ros3"
      name = "antenna_az"
      type = "antenna_az.py" />

  <node pkg = "necst_ros3"
    name = "antenna_az_feedback"
    type = "antenna_az_feedback.py" />

  <node pkg = "necst_ros3"
      name = "antenna_az_mapper"
      type = "antenna_az_mapper.py" />

  <node pkg = "necst_ros3"
      name = "antenna_az_lock"
      type = "antenna_az_lock.py" />

  <node pkg = "necst_ros3"
      name = "antenna_el"
      type = "antenna_el.py" />

  <node pkg = "necst_ros3"
      name = "antenna_el_feedback"
      type = "antenna_el_feedback.py" />

  <node pkg = "necst_ros3"
      name = "antenna_el_mapper"
      type = "antenna_el_mapper.py" />

  <node pkg = "necst_ros3"
      name = "antenna_el_lock"
      type = "antenna_el_lock.py" />

  <node pkg = "necst_ros3"
      name = "antenna_control"
      type = "antenna_control.py"
    <param name="name_topic_from" value="antenna_control_input_sim" />
  </node>

  <node pkg = "necst_ros3"
      name = "antenna_emergency"
      type = "antenna_emergency.py" />
    <param name="name_topic_from" value="antenna_emergency_input_sim" />
  </node>

</launch>