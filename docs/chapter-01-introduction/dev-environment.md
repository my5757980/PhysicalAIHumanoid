---
sidebar_position: 5
title: Development Environment Setup
---

# Development Environment Setup

This guide walks you through setting up a complete Physical AI development environment on Ubuntu 22.04.

## System Requirements

Before starting, ensure your system meets the minimum requirements:

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS (native) |
| CPU | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 |
| RAM | 16 GB | 32 GB |
| Storage | 100 GB SSD | 250 GB NVMe |
| GPU | Integrated | NVIDIA RTX 3070+ |

## Step 1: Update System

Start with a fresh system update:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git build-essential
```

## Step 2: Install ROS 2 Humble

ROS 2 Humble is the LTS release we'll use throughout this course.

### Add ROS 2 Repository

```bash
# Enable Universe repository
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS 2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Install ROS 2 Desktop

```bash
sudo apt update
sudo apt install ros-humble-desktop -y
```

### Install Development Tools

```bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-vcstool -y
```

### Initialize rosdep

```bash
sudo rosdep init
rosdep update
```

### Configure Shell

Add to your `~/.bashrc`:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify Installation

```bash
ros2 --version
# Should output: ros2 0.10.x
```

## Step 3: Install Gazebo Harmonic

Gazebo is our primary physics simulator.

```bash
# Add Gazebo repository
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install Gazebo Harmonic
sudo apt update
sudo apt install gz-harmonic -y
```

### Install ROS-Gazebo Bridge

```bash
sudo apt install ros-humble-ros-gz -y
```

### Verify Gazebo

```bash
gz sim --version
# Should output version info
```

## Step 4: Install Python Environment

We use Python 3.10+ for all code:

```bash
# Install Python tools
sudo apt install python3-pip python3-venv -y

# Create a virtual environment for the course
python3 -m venv ~/physical_ai_env
echo "source ~/physical_ai_env/bin/activate" >> ~/.bashrc
source ~/.bashrc

# Install essential packages
pip install --upgrade pip
pip install numpy scipy matplotlib pandas jupyter
pip install opencv-python pillow
pip install torch torchvision  # For AI work
```

## Step 5: Install Visual Studio Code

VS Code is our recommended editor:

```bash
# Download and install
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code -y
```

### Install Recommended Extensions

Open VS Code and install:

1. **ROS** (ms-iot.vscode-ros)
2. **Python** (ms-python.python)
3. **C/C++** (ms-vscode.cpptools)
4. **URDF** (smilerobotics.urdf)

## Step 6: Create ROS 2 Workspace

Set up your development workspace:

```bash
# Create workspace directory
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Build empty workspace
colcon build

# Source the workspace
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Step 7: Verify Complete Setup

Run this verification script:

```bash
# Create verification script
cat << 'EOF' > ~/verify_setup.sh
#!/bin/bash
echo "=== Physical AI Environment Verification ==="
echo ""

echo "1. Ubuntu Version:"
lsb_release -d
echo ""

echo "2. ROS 2 Version:"
ros2 --version
echo ""

echo "3. Gazebo Version:"
gz sim --version 2>/dev/null || echo "Gazebo not found"
echo ""

echo "4. Python Version:"
python3 --version
echo ""

echo "5. Key Python Packages:"
python3 -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python3 -c "import torch; print(f'PyTorch: {torch.__version__}')"
echo ""

echo "6. ROS 2 Workspace:"
if [ -d ~/ros2_ws ]; then
    echo "Workspace exists at ~/ros2_ws"
else
    echo "Workspace NOT found"
fi
echo ""

echo "=== Verification Complete ==="
EOF

chmod +x ~/verify_setup.sh
~/verify_setup.sh
```

## Directory Structure

Your final setup should look like:

```
~
├── ros2_ws/                  # ROS 2 workspace
│   ├── src/                  # Source packages
│   ├── build/                # Build artifacts
│   ├── install/              # Installed packages
│   └── log/                  # Build logs
├── physical_ai_env/          # Python virtual environment
└── .bashrc                   # Shell configuration
```

## Troubleshooting

### ROS 2 Commands Not Found

```bash
source /opt/ros/humble/setup.bash
```

### Gazebo Won't Start

Check for GPU issues:
```bash
glxinfo | grep "OpenGL"
```

### Python Package Conflicts

Use virtual environment:
```bash
source ~/physical_ai_env/bin/activate
```

### Permission Denied Errors

```bash
sudo usermod -aG dialout $USER  # For serial ports
sudo usermod -aG video $USER    # For cameras
# Log out and back in
```

## Next Steps

With your environment ready, you can:

1. Test ROS 2: `ros2 run demo_nodes_cpp talker`
2. Launch Gazebo: `gz sim shapes.sdf`
3. Begin Chapter 1 exercises

## Summary

You've set up a complete Physical AI development environment including:
- Ubuntu 22.04 LTS
- ROS 2 Humble
- Gazebo Harmonic
- Python with key packages
- VS Code with extensions

This environment will serve you throughout the course.

---

*Next: [Course Roadmap](./roadmap)*
