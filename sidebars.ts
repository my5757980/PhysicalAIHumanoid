import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  // Manual sidebar for the Physical AI & Humanoid Robotics textbook
  textbookSidebar: [
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics — AI-Native Textbook',
      link: { type: 'doc', id: 'intro' },
      items: [
        'intro',
        {
          type: 'category',
          label: 'Chapter 1: Introduction to Physical AI & Humanoid Robotics',
          link: { type: 'doc', id: 'chapter-1/index' },  // ✅ exact id match
          items: [
            'chapter-1/what-is-physical-ai',
            'chapter-1/humanoid-robots',
            'chapter-1/embodiment-perception-learning-control',
            'chapter-1/interdisciplinary-foundations',
            'chapter-1/real-world-examples'
          ]
        },
        {
          type: 'category',
          label: 'Chapter 2: Foundations of Robotics & Mechatronics',
          link: { type: 'doc', id: 'chapter-2/index' },  // ✅ exact id match
          items: [
            'chapter-2/kinematics-dynamics-dof',
            'chapter-2/sensors-actuators',
            'chapter-2/motor-control-torque-balance',
            'chapter-2/materials-structural-design',
            'chapter-2/mechatronic-integration'
          ]
        },
        {
          type: 'category',
          label: 'Chapter 3: AI for Embodied Intelligence',
          link: { type: 'doc', id: 'chapter-3/index' },  // ✅ exact id match
          items: [
            'chapter-3/computer-vision-slam',
            'chapter-3/decision-making-planning',
            'chapter-3/imitation-learning-teleoperation',
            'chapter-3/multimodal-models',
            'chapter-3/reinforcement-learning-control'
          ]
        },
        {
          type: 'category',
          label: 'Chapter 4: Humanoid Locomotion, Manipulation & Autonomy',
          link: { type: 'doc', id: 'chapter-4/index' },  // ✅ exact id match
          items: [
            'chapter-4/bipedal-walking-stability',
            'chapter-4/grippers-hands-manipulation',
            'chapter-4/whole-body-motion-control',
            'chapter-4/human-robot-interaction-safety',
            'chapter-4/autonomous-task-execution'
          ]
        }
      ]
    }
  ]
};

export default sidebars;
