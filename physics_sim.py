#!/usr/bin/env python3
"""
3D Physics Sandbox with PyBullet
- Press 'K' to spawn a cube with physics at the camera target.
- Press 'R' to reset the world (keep gravity & settings).
- Press 'ESC' or 'Q' to quit.

Requirements:
    pip install pybullet

Notes:
- Collisions are handled by the physics engine. This script also prints new contact events
  (object A touching object B) the first frame they occur to show collision detection is working.
"""

import time
import random
from collections import defaultdict

import pybullet as p
import pybullet_data


# ---------------------------- Config -------------------------------- #
TIMESTEP = 1.0 / 240.0
GRAVITY = -9.81

# Cube defaults
CUBE_SIZE = 0.25  # meters (edge length)
CUBE_MASS = 1.0   # kg
SPAWN_Z_OFFSET = 2.0  # meters above camera target
MAX_VELOCITY_JITTER = 1.5  # m/s random initial velocity

# Dynamics (materials)
DEFAULT_FRICTION = 0.8
DEFAULT_RESTITUTION = 0.1  # bounciness
DEFAULT_ROLLING_FRICTION = 0.001
DEFAULT_SPINNING_FRICTION = 0.001

# Key bindings
KEY_SPAWN = ord("k")
KEY_RESET = ord("r")
KEY_QUIT_Q = ord("q")
KEY_ESC = 27

# -------------------------------------------------------------------- #


def setup_world():
    cid = p.connect(p.GUI)
    if cid < 0:
        raise RuntimeError("Failed to open PyBullet GUI. If running headless, use p.DIRECT (no keyboard input).")
    p.resetDebugVisualizerCamera(cameraDistance=6.0, cameraYaw=45, cameraPitch=-30, cameraTargetPosition=[0, 0, 0])
    p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, GRAVITY)
    p.setTimeStep(TIMESTEP)

    plane = p.loadURDF("plane.urdf")  # has collision + visual
    p.changeDynamics(plane, -1,
                     lateralFriction=1.0,
                     restitution=0.0,
                     rollingFriction=0.0,
                     spinningFriction=0.0)

    return plane


def create_cube(size=CUBE_SIZE, mass=CUBE_MASS, position=(0, 0, 2), rgba=None):
    if rgba is None:
        rgba = [random.random()*0.6 + 0.4, random.random()*0.6 + 0.4, random.random()*0.6 + 0.4, 1.0]

    half = size / 2.0
    col_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[half, half, half])
    vis_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[half, half, half], rgbaColor=rgba)

    body_id = p.createMultiBody(baseMass=mass,
                                baseCollisionShapeIndex=col_id,
                                baseVisualShapeIndex=vis_id,
                                basePosition=position,
                                baseInertialFramePosition=[0, 0, 0])

    p.changeDynamics(body_id, -1,
                     lateralFriction=DEFAULT_FRICTION,
                     restitution=DEFAULT_RESTITUTION,
                     rollingFriction=DEFAULT_ROLLING_FRICTION,
                     spinningFriction=DEFAULT_SPINNING_FRICTION)

    # Tiny random spin/velocity for variety
    lin = [random.uniform(-MAX_VELOCITY_JITTER, MAX_VELOCITY_JITTER) for _ in range(3)]
    ang = [random.uniform(-2.0, 2.0) for _ in range(3)]
    p.resetBaseVelocity(body_id, linearVelocity=lin, angularVelocity=ang)
    return body_id


def get_camera_target():
    # getDebugVisualizerCamera returns 13 values:
    # [0]=width, [1]=height, [2]=viewMatrix, [3]=projectionMatrix,
    # [4]=cameraUp, [5]=cameraForward, [6]=hor, [7]=ver,
    # [8]=yaw, [9]=pitch, [10]=dist, [11]=target, [12]=camPos
    cam_info = p.getDebugVisualizerCamera()
    target = cam_info[11]  # cameraTargetPosition
    return target


def spawn_cube_at_camera_target():
    tx, ty, tz = get_camera_target()
    spawn_pos = [tx, ty, tz + SPAWN_Z_OFFSET]
    return create_cube(position=spawn_pos)


def key_was_triggered(events, key_code):
    return (key_code in events) and (events[key_code] & p.KEY_WAS_TRIGGERED)





def main():
    plane = setup_world()

    # Keep track of dynamic bodies so we can report contacts between them and others
    dynamic_bodies = set()

    # For collision event printing: track which pairs are already in contact this frame
    previous_contacts = set()

    print("3D Physics Sandbox ready.")
    print("Controls:")
    print("  K - spawn cube at camera target (drops from above)")
    print("  R - reset world (remove cubes)")
    print("  Q or ESC - quit")
    print()

    try:
        while True:
            events = p.getKeyboardEvents()

            if key_was_triggered(events, KEY_SPAWN):
                bid = spawn_cube_at_camera_target()
                dynamic_bodies.add(bid)
                print(f"Spawned cube id={bid}")

            if key_was_triggered(events, KEY_RESET):
                # remove all dynamic bodies
                for bid in list(dynamic_bodies):
                    try:
                        p.removeBody(bid)
                    except Exception:
                        pass
                dynamic_bodies.clear()
                p.resetBasePositionAndOrientation(plane, [0, 0, 0], [0, 0, 0, 1])
                print("World reset.")

            if key_was_triggered(events, KEY_QUIT_Q) or key_was_triggered(events, KEY_ESC):
                print("Exiting.")
                break

            # Step the simulation
            p.stepSimulation()

            # --- Collision reporting (first-touch events) ---
            # Build current contact pairs set
            current_contacts = set()
            for cp in p.getContactPoints():
                a = cp[1]  # bodyUniqueIdA
                b = cp[2]  # bodyUniqueIdB
                # Normalize pair order to avoid duplicates
                pair = (min(a, b), max(a, b))
                current_contacts.add(pair)

            # Report newly started contacts (present now, absent previously)
            new_contacts = current_contacts - previous_contacts
            for a, b in sorted(new_contacts):
                # Optional filtering: only print if at least one is dynamic (not the plane), to reduce spam
                if a in dynamic_bodies or b in dynamic_bodies:
                    print(f"[Contact] {a} <-> {b}")

            previous_contacts = current_contacts

            time.sleep(TIMESTEP)  # real-time pacing

    finally:
        p.disconnect()


if __name__ == "__main__":
    main()
