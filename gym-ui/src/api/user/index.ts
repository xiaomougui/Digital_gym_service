import request from "@/tool/request";

import type UserDetails from "@/types/userDetails";

interface passwordForm {
    id: number,
    old_password: string,
    new_password: string,
}

// 定义基础URL常量
const BASE_URL = "http://127.0.0.1:8000/user";

export default class UserService {
    /**
     * 获取个人信息
     * @param id 
     * @returns 
     */
    getUserDetails(id: number): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/info/${id}`,
        });
    }
    /**
     * 修改个人信息
     * @param details 
     * @returns 
     */
    modifyUserDetails(details: UserDetails): Promise<any> {
        console.log(details);
        return request({
            method: "post",
            url: `${BASE_URL}/update`,
            data: details
        });
    }

    /**
     * 修改密码
     * @param passwordObj 
     * @returns 
     */
    modfiyPassword(passwordObj: passwordForm): Promise<any> {
        return request({
            method: "post",
            url: `${BASE_URL}/updatepassword`,
            data: passwordObj
        });
    }

    /**
     * 获取用户列表
     * @returns 
     */
    getUserList(): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/list`,
        });
    }

}