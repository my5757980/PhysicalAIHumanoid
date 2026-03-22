import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function HeroSection(): JSX.Element {
  return (
    <section className={styles.hero}>
      <div className={styles.heroOverlay}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>
            Physical AI & Humanoid Robotics
          </h1>
          <p className={styles.heroSubtitle}>
            AI-Native Textbook for Embodied Intelligence
          </p>
          <p className={styles.heroDescription}>
            Master ROS 2, Gazebo, Unity, and NVIDIA Isaac to build intelligent humanoid robots
            that bridge digital AI with physical embodiments.
          </p>
          <div className={styles.heroButtons}>
            <Link
              className={styles.heroPrimaryButton}
              to="/docs/intro">
              Start Learning
            </Link>
            <Link
              className={styles.heroSecondaryButton}
              to="/docs/chapter-01-introduction">
              View Chapters
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
