import { defineStore } from 'pinia'
import type { User } from '@/types/user'
import { childrenRoutes } from '@/router/index'
import type { RoutForm, InputRoute } from '@/types/routform'

interface AuthState {
    user: User | null
    token: string | null
    permissionRoutes: Array<RoutForm> | null
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: null,
        token: null,
        permissionRoutes: null,
    }),
    getters: {
        isAuthenticated: state => !!state.token,
        isAdmin: state => state.user?.permission_level === 'admin',
        isSuperadmin: state => state.user?.permission_level === 'superadmin'
    },
    actions: {
        //填入信息
        fillInforamtion(userInfo: User) {
            // 实际调用API
            this.user = userInfo;
            // this.token = 'mock-token'
        },
        logout() {
            this.user = null
            this.token = null
        },
        filterRoutesByLevel() {
            this.permissionRoutes = transformRoutes(this.user?.permission_level!, childrenRoutes, '/main');
            console.log(this.permissionRoutes, 'authstore')
        }
    },
    persist: true // 使用持久化插件
})


/**
 * 转换路由配置的函数
 * @param role 当前用户权限
 * @param routes 原始路由配置
 * @param parentPath 父级路径（内部递归使用）
 */
function transformRoutes(
    role: string,
    routes: InputRoute[],
    parentPath: string = ''
): Array<RoutForm> {
    return routes
        .filter(route => {
            // 权限过滤：检查roles是否包含当前权限
            const hasPermission = !route.meta.roles || route.meta.roles.includes(role)
            // 管理员权限检查
            const isAdminAllowed = !route.meta.requiresAdmin || ['admin', 'superadmin'].includes(role)
            return hasPermission && isAdminAllowed
        })
        .map(route => {
            const fullPath = parentPath ? `${parentPath}/${route.path}` : `/${route.path}`
            return {
                path: fullPath,
                title: route.meta.title,
                icon: route.meta.icon,
                children: route.children
                    ? transformRoutes(role, route.children, fullPath)
                    : null
            }
        })
}

// let arr: Array<RoutForm> = [{
//     path: '/user',
//     title: "用户",
//     children: [
//         {
//             path: '/user/profile',
//             title: "个人信息",
//             children: null
//         }, {
//             path: '/user/manage',
//             title: "用户管理",
//             children: null
//         }
//     ]
// }]