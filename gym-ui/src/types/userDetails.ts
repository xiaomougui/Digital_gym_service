// 定义权限等级枚举
type PermissionLevel = 'superadmin' | 'admin' | 'common';

// 定义性别枚举
type Gender = '男' | '女';

// 用户类型定义
export default interface UserDetails {
    id: number;
    username?: string;
    password?: string;
    email?: string;
    phone?: string | null;  // 联系电话（可选）
    real_name?: string | null;  // 真实姓名（可选）
    avatar?: string | null;  // 头像URL或Base64编码（可选）
    gender?: Gender;
    permission_level: 'superadmin' | 'admin' | 'common';
    id_card?: string
}

// 可选的创建用户DTO（用于创建新用户）
interface CreateUserDto {
    username: string;
    password: string;
    email: string;
    phone?: string;
    real_name?: string;
    avatar?: string;
    balance?: number;
    status?: boolean;
    permission_level?: PermissionLevel;
    gender?: Gender;
}

// 可选的更新用户DTO（用于更新用户信息）
interface UpdateUserDto {
    username?: string;
    password?: string;
    email?: string;
    phone?: string | null;
    real_name?: string | null;
    avatar?: string | null;
    balance?: number;
    status?: boolean;
    last_login?: Date | string | null;
    permission_level?: PermissionLevel;
    gender?: Gender;
}