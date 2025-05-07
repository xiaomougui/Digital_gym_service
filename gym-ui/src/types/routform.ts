interface RoutForm {
    title: string,
    path: string,
    icon?: string,
    children: Array<RoutForm> | null
}

interface InputRoute {
    path: string
    meta: { title: string; roles?: string[]; requiresAdmin?: boolean; icon?: string }
    children?: Array<InputRoute>
    component?: any
}

export type {
    RoutForm,
    InputRoute
}