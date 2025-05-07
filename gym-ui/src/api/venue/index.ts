import request from "@/tool/request";

// 枚举定义 - 与后端模型完全一致
enum VenueType {
    BASKETBALL = 'basketball',
    BADMINTON = 'badminton',
    SWIMMING = 'swimming',
    GYM = 'gym',
    TENNIS = 'tennis'
}

enum VenueStatus {
    ACTIVE = 'active',
    MAINTENANCE = 'maintenance',
    CLOSED = 'closed'
}

enum ReservationStatus {
    PENDING = 'pending',
    CONFIRMED = 'confirmed',
    CANCELLED = 'cancelled',
    COMPLETED = 'completed'
}

// 接口定义 - 严格匹配SQLAlchemy模型
interface Venue {
    name: string;
    type: VenueType;
    capacity: number;
    total_count: number;
    available_count: number;
    open_time: string;  // 格式: "HH:MM:SS"
    close_time: string;
    status: VenueStatus;
    location?: string;
    description?: string;
    created_at?: string;
    updated_at?: string;
}

interface Reservation {
    user_id: number;
    venue_id: number;
    start_time: string;  // ISO 8601格式
    end_time: string;
    status: ReservationStatus;
    notes?: string;
    created_at?: string;
    updated_at?: string;
    venue?: Venue;  // 关联数据
}

interface CreateVenueData {
    name: string;
    type: VenueType;
    capacity: number;
    total_count: number;
    available_count: number;
    open_time: string;
    close_time: string;
    status?: VenueStatus;
    location?: string;
    description?: string;
}

interface UpdateVenueData {
    id: number;
    name?: string;
    type?: VenueType;
    capacity?: number;
    total_count?: number;
    available_count?: number;
    open_time?: string;
    close_time?: string;
    status?: VenueStatus;
    location?: string;
    description?: string;
}

interface CreateReservationData {
    venue_id: number;
    user_id: number;
    start_time: string;
    end_time: string;
    notes?: string;
}

const BASE_URL = "http://127.0.0.1:8000/venue";

export default class VenueService {
    /**
     * 获取场馆列表
     * @returns Promise<Venue[]> 场馆列表
     */
    static getVenues(): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/info`
        });
    }

    /**
     * 创建场馆 (管理员)
     * @param data 场馆数据
     * @returns Promise<{code: number, msg: string}>
     */
    static createVenue(data: CreateVenueData): Promise<any> {
        return request({
            method: "post",
            url: `${BASE_URL}/create`,
            data
        });
    }

    /**
     * 更新场馆信息 (管理员)
     * @param data 场馆数据
     * @returns Promise<{code: number, msg: string}>
     */
    static updateVenue(data: UpdateVenueData): Promise<any> {
        return request({
            method: "post",
            url: `${BASE_URL}/update`,
            data
        });
    }

    /**
     * 删除场馆 (管理员)
     * @param id 场馆ID
     * @returns Promise<{code: number, msg: string}>
     */
    static deleteVenue(id: number): Promise<any> {
        return request({
            method: "delete",
            url: `${BASE_URL}/delete/${id}`
        });
    }

    /**
     * 创建预约
     * @param data 预约数据
     * @returns Promise<{code: number, msg: string}>
     */
    static createReservation(data: CreateReservationData): Promise<any> {
        return request({
            method: "post",
            url: `${BASE_URL}/reservation`,
            data
        });
    }

    /**
     * 获取我的预约列表
     * @param userId 用户ID
     * @returns Promise<Reservation[]> 预约列表
     */
    static getMyReservations(userId: number): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/my_reservation/${userId}`
        });
    }

    /**
     * 获取所有预约详情 (管理员)
     * @param permissionLevel 权限级别
     * @returns Promise<Reservation[] | {code: number, msg: string}>
     */
    static getAllReservations(permissionLevel: string): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/reservation_detail/${permissionLevel}`
        });
    }

    /**
     * 取消预约
     * @param id 预约ID
     * @returns Promise<{code: number, msg: string}>
     */
    static cancelReservation(id: number): Promise<any> {
        return request({
            method: "put",
            url: `${BASE_URL}/cancel_reservation/${id}`
        });
    }
}

// 导出枚举类型
export { VenueType, VenueStatus, ReservationStatus };