interface User {
    id: number,
    username: string,
    avatar: string,
    // permission_id: number
    permission_level: 'superadmin' | 'admin' | 'common'
}

export type {
    User
}