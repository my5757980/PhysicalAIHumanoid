import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HeroSection from '@site/src/components/HeroSection';

import styles from './index.module.css';

// Chapter data for the homepage
const chapters = [
  {
    number: 1,
    title: 'Introduction to Physical AI',
    description: 'Explore the fundamentals of Physical AI and embodied intelligence.',
    link: '/docs/chapter-01-introduction',
  },
  {
    number: 2,
    title: 'Foundations of Humanoid Robotics',
    description: 'Learn humanoid anatomy, kinematics, sensors, and actuators.',
    link: '/docs/chapter-02-foundations',
  },
  {
    number: 3,
    title: 'ROS 2: The Robotic Nervous System',
    description: 'Master ROS 2 middleware for robotic control systems.',
    link: '/docs/chapter-03-ros2-basics',
  },
  {
    number: 4,
    title: 'ROS 2 Advanced',
    description: 'Dive deep into services, URDF, TF2, and navigation.',
    link: '/docs/chapter-04-ros2-advanced',
  },
  {
    number: 5,
    title: 'Robot Simulation with Gazebo',
    description: 'Build physics-based simulations and virtual environments.',
    link: '/docs/chapter-05-gazebo',
  },
  {
    number: 6,
    title: 'Unity for High-Fidelity Simulation',
    description: 'Create photorealistic simulations with Unity Robotics Hub.',
    link: '/docs/chapter-06-unity',
  },
  {
    number: 7,
    title: 'NVIDIA Isaac Platform',
    description: 'Leverage Isaac Sim, Isaac ROS, and Isaac Gym.',
    link: '/docs/chapter-07-nvidia-isaac',
  },
  {
    number: 8,
    title: 'AI-Powered Perception & Manipulation',
    description: 'Implement computer vision and reinforcement learning.',
    link: '/docs/chapter-08-perception-manipulation',
  },
  {
    number: 9,
    title: 'Humanoid Robot Development',
    description: 'Master VLA, kinematics, locomotion, and interaction.',
    link: '/docs/chapter-09-humanoid-development',
  },
  {
    number: 10,
    title: 'Conversational Robotics & Capstone',
    description: 'Build voice-controlled robots and complete your capstone.',
    link: '/docs/chapter-10-conversational-capstone',
  },
];

function ChapterCard({number, title, description, link}: {
  number: number;
  title: string;
  description: string;
  link: string;
}): JSX.Element {
  return (
    <Link to={link} className={styles.chapterCard}>
      <div className={styles.chapterNumber}>Chapter {number}</div>
      <h3 className={styles.chapterTitle}>{title}</h3>
      <p className={styles.chapterDescription}>{description}</p>
    </Link>
  );
}

function ChaptersSection(): JSX.Element {
  return (
    <section className={styles.chaptersSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Explore the Chapters</h2>
        <p className={styles.sectionSubtitle}>
          10 comprehensive chapters covering the complete Physical AI & Humanoid Robotics curriculum
        </p>
        <div className={styles.chaptersGrid}>
          {chapters.map((chapter) => (
            <ChapterCard key={chapter.number} {...chapter} />
          ))}
        </div>
      </div>
    </section>
  );
}

function FeaturesSection(): JSX.Element {
  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <div className={styles.featuresGrid}>
          <div className={styles.featureItem}>
            <h3>ROS 2 Mastery</h3>
            <p>Learn the robotic middleware that powers modern autonomous systems.</p>
          </div>
          <div className={styles.featureItem}>
            <h3>Simulation First</h3>
            <p>Build and test in Gazebo, Unity, and NVIDIA Isaac before real deployment.</p>
          </div>
          <div className={styles.featureItem}>
            <h3>AI Integration</h3>
            <p>Connect GPT models, computer vision, and reinforcement learning to robots.</p>
          </div>
          <div className={styles.featureItem}>
            <h3>Hands-On Projects</h3>
            <p>Complete practical projects and a capstone autonomous humanoid.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Physical AI & Humanoid Robotics Textbook"
      description="AI-Native Textbook for the Physical AI & Humanoid Robotics Course. Master ROS 2, Gazebo, Unity, and NVIDIA Isaac.">
      <HeroSection />
      <main>
        <FeaturesSection />
        <ChaptersSection />
      </main>
    </Layout>
  );
}
