import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth.ts'

// 公共组件
const Login = () => import('@/views/login/login.vue')
// const EmptyLayout = () => import('@/layouts/EmptyLayout.vue')



export const childrenRoutes = [

    // --- 用户管理模块 ---
    {
        path: 'user',
        meta: { title: '用户', roles: ['admin', 'superadmin', 'common'], icon: "User" },
        children: [
            {
                path: 'profile',
                component: () => import('@/views/user/profile.vue'),
                meta: { title: '个人信息', roles: ['admin', 'superadmin', 'common'] }
            },
            {
                path: 'management',
                component: () => import('@/views/user/manage.vue'),
                meta: { title: '用户管理', roles: ['admin', 'superadmin'] }
            }
        ]
    },
    // --- 赛事模块 ---
    {
        path: 'event',
        meta: { title: '赛事', roles: ['admin', 'superadmin', 'common'], icon: "Medal" },
        children: [
            {
                path: 'join',
                component: () => import('@/views/event/join.vue'),
                meta: { title: '参加赛事', roles: ['admin', 'superadmin', 'common'] },
                props: true
            },
            {
                path: 'my',
                component: () => import('@/views/event/my.vue'),
                // meta: { title: '创建赛事', requiresAdmin: true }
                meta: { title: '我的赛事', roles: ['admin', 'superadmin', 'common'] }
            },
            {
                path: 'manage',
                component: () => import('@/views/event/manage.vue'),
                meta: { title: '赛事管理', roles: ['admin', 'superadmin'] }
            },
            {
                path: 'result/:id',
                component: () => import('@/views/event/result.vue'),
                meta: { title: '赛事结果', roles: ['admin', 'superadmin', 'common'] },
                props: true
            },
            {
                path: 'details/:id',
                component: () => import('@/views/event/details.vue'),
                meta: { title: '赛事详情', roles: ['admin', 'superadmin', 'common'] },
                props: true
            }
        ]
    },

    // --- 场馆模块 ---
    {
        path: 'venue',
        meta: { title: '场馆', roles: ['admin', 'superadmin', 'common'], icon: "House" },
        children: [
            {
                path: 'reservation',
                component: () => import('@/views/venue/reservation.vue'),
                meta: { title: '场馆预约', roles: ['admin', 'superadmin', 'common'] }
            },
            {
                path: 'my-reservations',
                component: () => import('@/views/venue/my.vue'),
                meta: { title: '我的预约', roles: ['admin', 'superadmin', 'common'] }
            },
            {
                path: 'management',
                component: () => import('@/views/venue/manage.vue'),
                meta: { title: '场馆管理', roles: ['admin', 'superadmin'] }
            },
            {
                path: 'status',
                component: () => import('@/views/venue/status.vue'),
                meta: { title: '预约情况', roles: ['admin', 'superadmin'] }
            }
        ]
    },

    // --- 设备模块 ---
    {
        path: 'equipment',
        meta: { title: "设备", roles: ['admin', 'superadmin', 'common'], icon: "Baseball" },
        children: [
            {
                path: 'rental',
                component: () => import('@/views/equipment/rental.vue'),
                meta: { title: '设备租赁', roles: ['admin', 'superadmin', 'common'] }
            },
            {
                path: 'my-rentals',
                component: () => import('@/views/equipment/my.vue'),
                meta: { title: '我的租赁', roles: ['admin', 'superadmin', 'common'] }
            },
            {
                path: 'management',
                component: () => import('@/views/equipment/manage.vue'),
                meta: { title: '设备管理', roles: ['admin', 'superadmin'] }
            },
            {
                path: 'status',
                component: () => import('@/views/equipment/status.vue'),
                meta: { title: '租赁情况', roles: ['admin', 'superadmin'] }
            }
        ]
    },

    // --- 反馈模块 ---
    {
        path: 'feedback',
        meta: { title: "反馈", roles: ['admin', 'superadmin', 'common'], icon: "Message" },
        children: [
            {
                path: 'my-feedback',
                component: () => import('@/views/feedback/my.vue'),
                meta: { title: '我的反馈', roles: ['admin', 'superadmin', 'common'] }
            },
            {
                path: 'management',
                component: () => import('@/views/feedback/manage.vue'),
                meta: { title: '反馈管理', roles: ['admin', 'superadmin'] }
            }
        ]
    },

    // --- 数据报表 ---
    // {
    //     path: 'report',
    //     meta: { title: "报表", roles: ['admin', 'superadmin'], icon: "PieChart" },
    //     children: [
    //         {
    //             path: 'venue',
    //             component: () => import('@/views/report/venue.vue'),
    //             meta: { title: '场馆报表', roles: ['admin', 'superadmin'] }
    //         },
    //         {
    //             path: 'foot-traffic',
    //             component: () => import('@/views/report/traffic.vue'),
    //             meta: { title: '人流量统计', roles: ['admin', 'superadmin'] }
    //         },
    //         {
    //             path: 'equipment',
    //             component: () => import('@/views/report/equipment.vue'),
    //             meta: { title: '设备报表', roles: ['admin', 'superadmin'] }
    //         }
    //     ]
    // }
]

// 动态路由配置
const routes: RouteRecordRaw[] = [
    {
        path: '/login',
        component: () => import('@/views/login/login.vue'),
        meta: { title: '登录', roles: ['admin', 'superadmin', 'common'] }
    },
    {
        path: '/main',
        component: () => import('@/components/layout/Main.vue'),
        meta: { title: '控制台', roles: ['admin', 'superadmin', 'common'] },
        children: [
            // 仪表盘
            ...childrenRoutes
        ]
    }
]




//     // --- 登录/登出 ---
//     {
//         path: '/auth',
//         component: EmptyLayout,
//         children: [
//             {
//                 path: 'login',
//                 component: () => import('@/views/auth/Login.vue'),
//                 meta: { title: '登录', guestOnly: true }
//             },
//             {
//                 path: 'logout',
//                 redirect: to => {
//                     const auth = useAuthStore()
//                     auth.logout()
//                     return '/auth/login'
//                 }
//             }
//         ]
//     },

//     // 404 处理
//     {
//         path: '/:pathMatch(.*)*',
//         component: () => import('@/views/NotFound.vue'),
//         meta: { title: '页面不存在' }
//     }
// ]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

// 路由守卫 - 权限控制
router.beforeEach((to, from, next) => {
    if (to.path === '/') {
        return next('/login') // 手动重定向
    }
    const auth = useAuthStore()
    const isAdmin = auth.user?.permission_level === 'admin'

    // 需要登录但未登录
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return next({ path: '/auth/login', query: { redirect: to.fullPath } })
    }

    // 需要管理员权限但非管理员
    if (to.meta.requiresAdmin && !isAdmin) {
        return next({ path: '/dashboard' })
    }

    // 游客专属页面（如登录页）
    if (to.meta.guestOnly && auth.isAuthenticated) {
        return next('/dashboard')
    }

    next()
})

export default router