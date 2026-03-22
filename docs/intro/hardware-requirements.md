---
sidebar_position: 3
title: Hardware Requirements
---

# Hardware Requirements

This course uses a **simulation-first approach**, meaning most exercises can be completed without physical hardware. However, optional physical builds enhance the learning experience.

## Development Machine

### Minimum Requirements

| Component | Specification |
|-----------|--------------|
| **OS** | Ubuntu 22.04 LTS (or WSL2 on Windows 11) |
| **CPU** | Intel Core i5 / AMD Ryzen 5 or better |
| **RAM** | 16 GB minimum |
| **Storage** | 100 GB free SSD space |
| **GPU** | Integrated graphics (for Modules 1-2) |

### Recommended Requirements

| Component | Specification |
|-----------|--------------|
| **OS** | Ubuntu 22.04 LTS (native, not WSL) |
| **CPU** | Intel Core i7 / AMD Ryzen 7 or better |
| **RAM** | 32 GB |
| **Storage** | 250 GB free NVMe SSD |
| **GPU** | NVIDIA RTX 3070 or better (Required for Module 3+) |

### NVIDIA GPU Requirements

For Isaac Sim and deep learning (Chapters 7-10):

- **Minimum**: RTX 2070 / RTX 3060 (8GB VRAM)
- **Recommended**: RTX 3080 / RTX 4070 (12GB+ VRAM)
- **Driver**: 525.x or newer
- **CUDA**: 11.8 or 12.x

## Software Stack

### Core Software

| Software | Version | Purpose |
|----------|---------|---------|
| ROS 2 | Humble | Robot middleware |
| Gazebo | Harmonic | Physics simulation |
| Unity | 2022.3 LTS | High-fidelity simulation |
| Isaac Sim | 2023.1+ | NVIDIA simulation |
| Python | 3.10+ | Programming |
| PyTorch | 2.0+ | Deep learning |

### Development Tools

- Visual Studio Code with ROS extension
- Git for version control
- Docker (optional, for containerized builds)

## Optional Physical Hardware

### Starter Kit (~$200-300)

For basic physical experiments:

| Component | Example | Purpose |
|-----------|---------|---------|
| Single-Board Computer | Raspberry Pi 5 | Edge computing |
| Depth Camera | Intel RealSense D435 | 3D perception |
| Servo Motors | Dynamixel AX-12A | Joint actuation |
| IMU | BNO055 | Orientation sensing |

### Advanced Kit (~$500-1000)

For full humanoid prototype:

| Component | Example | Purpose |
|-----------|---------|---------|
| Edge AI Computer | NVIDIA Jetson Orin Nano | On-robot AI |
| Stereo Camera | ZED 2 | High-quality depth |
| Robot Arm | Interbotix WidowX 250 | Manipulation |
| Lidar | RPLidar A1 | 2D mapping |

### Full Humanoid Platform (~$5000+)

For serious development:

| Platform | Description |
|----------|-------------|
| Unitree G1 | Entry-level humanoid |
| Figure 01 Dev Kit | Advanced humanoid (when available) |
| Custom Build | 3D printed with Dynamixel servos |

## Cloud Alternatives

If your local machine doesn't meet requirements:

### For Isaac Sim

- **NVIDIA Omniverse Cloud**: Run Isaac Sim in the cloud
- **AWS RoboMaker**: Cloud-based simulation
- **Google Cloud**: GPU instances for training

### For Development

- **GitHub Codespaces**: Cloud VS Code environment
- **Paperspace Gradient**: GPU notebooks
- **Lambda Labs**: Affordable GPU cloud

## Architecture Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Machine                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   ROS 2     │  │   Gazebo    │  │    Isaac Sim        │  │
│  │   Humble    │  │   Harmonic  │  │    (NVIDIA GPU)     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┴─────────────────────┘             │
│                          │                                   │
│                    ROS 2 Bridge                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │    Optional: Physical   │
              │        Robot            │
              │  ┌─────────────────┐    │
              │  │  Jetson Orin    │    │
              │  │  + Sensors      │    │
              │  │  + Actuators    │    │
              │  └─────────────────┘    │
              └─────────────────────────┘
```

## Verification Checklist

Run these commands to verify your setup:

```bash
# Check Ubuntu version
lsb_release -a

# Check Python version
python3 --version

# Check GPU (if NVIDIA)
nvidia-smi

# Check available memory
free -h

# Check disk space
df -h
```

---

*Ready to see the assessment structure? Continue to [Assessments](./assessments)*
