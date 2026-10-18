from coconut_harvest_robot.sensor_quality import SensorObservation, SensorStatus, assess_sensor_health

def test_sensor_health_ok():
    r = assess_sensor_health([
        SensorObservation("rgb", True, 0.95, 1.0),
        SensorObservation("depth", True, 0.90, 1.02),
    ])
    assert r.status == SensorStatus.OK

def test_sensor_health_detects_timestamp_skew():
    r = assess_sensor_health([
        SensorObservation("rgb", True, 1.0, 1.0, 0.05),
        SensorObservation("depth", True, 1.0, 1.2, 0.05),
    ])
    assert r.status == SensorStatus.UNSYNCHRONIZED
