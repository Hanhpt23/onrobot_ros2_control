import pyspacemouse
import time

device = pyspacemouse.open(
    axis_convention=pyspacemouse.AxisConvention.ROS
)

if device is None:
    print("Could not open SpaceMouse")
    exit()

print("SpaceMouse Connected")

try:
    while True:
        state = device.read()

        pressed = [
            i for i, value in enumerate(state.buttons)
            if value
        ]

        if state is not None:
            print(
                f"x={state.x:+.3f} "
                f"y={state.y:+.3f} "
                f"z={state.z:+.3f} "
                f"roll={state.roll:+.3f} "
                f"pitch={state.pitch:+.3f} "
                f"yaw={state.yaw:+.3f} "
                f"Pressed buttons: {pressed}"
            )

except KeyboardInterrupt:
    pass

finally:
    device.close()