import { defineConfig } from 'vitepress'

export default defineConfig({
    title: 'WeChat Weather Push',
    description: '微信每日天气推送系统文档',

    base: '/Wechat_Weather/',

    locales: {
        'zh': {
            label: '中文',
            lang: 'zh-CN',
            link: '/zh/',
            themeConfig: {
                nav: [
                    { text: '首页', link: '/zh/' },
                    { text: '指南', link: '/zh/guide/overview' },
                ],
                sidebar: [
                    {
                        text: '入门',
                        items: [
                            { text: '项目概述', link: '/zh/guide/overview' },
                            { text: '快速开始', link: '/zh/guide/quickstart' },
                        ]
                    },
                    {
                        text: '详细说明',
                        items: [
                            { text: '代码架构', link: '/zh/guide/architecture' },
                            { text: '推送流程', link: '/zh/guide/push-flow' },
                            { text: 'GitHub Actions', link: '/zh/guide/github-actions' },
                        ]
                    },
                ],
                outline: {
                    label: '页面导航',
                },
            },
        },
        'en': {
            label: 'English',
            lang: 'en-US',
            link: '/en/',
            themeConfig: {
                nav: [
                    { text: 'Home', link: '/en/' },
                    { text: 'Guide', link: '/en/guide/overview' },
                ],
                sidebar: [
                    {
                        text: 'Getting Started',
                        items: [
                            { text: 'Overview', link: '/en/guide/overview' },
                            { text: 'Quick Start', link: '/en/guide/quickstart' },
                        ]
                    },
                    {
                        text: 'Details',
                        items: [
                            { text: 'Architecture', link: '/en/guide/architecture' },
                            { text: 'Push Flow', link: '/en/guide/push-flow' },
                            { text: 'GitHub Actions', link: '/en/guide/github-actions' },
                        ]
                    },
                ],
            },
        },
    },

    themeConfig: {
        socialLinks: [
            { icon: 'github', link: 'https://github.com/HuangShengZeBlueSky/Wechat_Weather' }
        ],
    },
})
