// docusaurus.config.ts
import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import webpack from 'webpack';

// ✅ Load .env variables
require('dotenv').config();

const config: Config = {
  title: 'Physical AI & Humanoid Robotics — AI-Native Textbook',
  tagline: 'Comprehensive textbook on embodied intelligence and humanoid robotics',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://my5757980.github.io',
  baseUrl: '/PhysicalAIHumanoid/',

  organizationName: 'my5757980',
  projectName: 'PhysicalAIHumanoid',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/my5757980/PhysicalAIHumanoid/tree/main/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/my5757980/PhysicalAIHumanoid/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  // ✅ Plugin to expose VITE environment variables for frontend
  plugins: [
    function envPlugin() {
      return {
        name: 'env-plugin',
        configureWebpack() {
          return {
            plugins: [
              new webpack.DefinePlugin({
                'import.meta.env.VITE_BACKEND_URL': JSON.stringify(process.env.VITE_BACKEND_URL),
                'import.meta.env.VITE_QDRANT_COLLECTION': JSON.stringify(process.env.VITE_QDRANT_COLLECTION),
              }),
            ],
          };
        },
      };
    },
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'textbookSidebar',
          position: 'left',
          label: 'Textbook',
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/my5757980/PhysicalAIHumanoid',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Textbook',
          items: [
            { label: 'Introduction', to: '/docs/intro' },
            { label: 'Chapter 1', to: '/docs/chapter-1' },
            { label: 'Chapter 2', to: '/docs/chapter-2' },
            { label: 'Chapter 3', to: '/docs/chapter-3' },
            { label: 'Chapter 4', to: '/docs/chapter-4' },
          ],
        },
        {
          title: 'Resources',
          items: [
            { label: 'Docusaurus', href: 'https://docusaurus.io' },
            { label: 'GitHub', href: 'https://github.com/facebook/docusaurus' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
