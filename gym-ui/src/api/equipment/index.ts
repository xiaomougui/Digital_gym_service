import request from "@/tool/request";
import type { Equipment, Rental } from '@/types/equipment'


// 定义基础URL常量
const BASE_URL = "http://127.0.0.1:8000/equipment";

export default class EquipmentService {
    /**
     * 获取设备列表
     * @returns Promise
     */
    static getEquipmentList(): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/list`,
        });
    }

    /**
     * 添加设备
     * @param equipment 设备信息
     * @returns Promise
     */
    static addEquipment(equipment: Equipment): Promise<any> {
        return request({
            method: "post",
            url: `${BASE_URL}/add`,
            data: equipment,
        });
    }

    /**
     * 更新设备信息
     * @param equipmentId 设备ID
     * @param equipment 设备信息
     * @returns Promise
     */
    static updateEquipment(equipmentId: number, equipment: Equipment): Promise<any> {
        return request({
            method: "post",
            url: `${BASE_URL}/update-equipment/${equipmentId}`,
            data: equipment,
        });
    }

    /**
     * 删除设备
     * @param equipmentId 设备ID
     * @returns Promise
     */
    static deleteEquipment(equipmentId: number): Promise<any> {
        return request({
            method: "delete",
            url: `${BASE_URL}/delete-equipment/${equipmentId}`,
        });
    }

    /**
     * 获取我的租赁列表
     * @param userId 用户ID
     * @returns Promise
     */
    static getMyRentals(userId: number): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/my-rentals`,
            params: { user_id: userId },
        });
    }

    /**
     * 租赁设备
     * @param rental 租赁信息
     * @returns Promise
     */
    static rentEquipment(rental: Rental): Promise<any> {
        return request({
            method: "post",
            url: `${BASE_URL}/rental`,
            data: rental,
        });
    }

    /**
     * 取消租赁
     * @param rentalId 租赁ID
     * @returns Promise
     */
    static cancelRental(rentalId: number): Promise<any> {
        return request({
            method: "put",
            url: `${BASE_URL}/cancel-rental/${rentalId}`,
        });
    }

    /**
     * 归还设备
     * @param rentalId 租赁ID
     * @returns Promise
     */
    static returnEquipment(rentalId: number): Promise<any> {
        return request({
            method: "put",
            url: `${BASE_URL}/return-equipment/${rentalId}`,
        });
    }

    /**
     * 获取所有租赁记录
     * @returns Promise
     */
    static getAllRentals(): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/rentals`,
        });
    }
}