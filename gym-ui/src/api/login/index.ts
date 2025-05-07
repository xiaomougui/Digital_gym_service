import request from "@/tool/request";
import getClientId from "./clientId";

// 定义基础URL常量
const BASE_URL = "http://127.0.0.1:8000/auth";

// 定义接口类型
interface LoginParams {
    username: string;
    password: string;
    captcha: string;
}

interface RegisterParams {
    username: string;
    password: string;
    captcha: string;
    email: string;
}

// 使用class封装登录相关API
export default class LoginService {
    /**
     * 获取验证码图片
     */
    getVerifyImg(): Promise<any> {
        return request({
            method: "get",
            url: `${BASE_URL}/login/captcha`,
            headers: {
                "X-Client-ID": getClientId()
            }
        });
    }

    /**
     * 验证登录信息
     * @param params 登录参数
     */
    checkLogin(params: LoginParams): Promise<any> {
        const formData = new URLSearchParams();
        formData.append('username', params.username);
        formData.append('password', params.password);
        formData.append('captcha', params.captcha);

        return request({
            url: `${BASE_URL}/login`,
            method: "post",
            data: formData,
            headers: {
                "X-Client-ID": getClientId(),
            }
        });
    }

    /**
     * 开始注册
     * @param params 注册参数
     */
    startRegister(params: RegisterParams): Promise<any> {
        const formData = new URLSearchParams();
        formData.append('username', params.username);
        formData.append('captcha', params.captcha);
        formData.append('password', params.password);
        formData.append('email', params.email);

        return request({
            url: `${BASE_URL}/register`,
            method: "post",
            data: formData,
        });
    }

    /**
     * 获取邮箱验证码
     * @param email 邮箱地址
     */
    getEmailCode(email: string): Promise<any> {
        const formData = new URLSearchParams();
        formData.append('email', email);
        return request({
            url: `${BASE_URL}/email/captcha`,
            method: "post",
            data: { email },
        });
    }
}