import request from "@/tool/request";

// 定义反馈接口数据类型
interface Feedback {
    id?: number;
    user_id: number;
    message: string;
    solved?: boolean;
    reason?: string;
    created_at?: string;
}

// 定义反馈列表响应类型
interface FeedbackListResponse {
    code: number;
    data: Feedback[];
    msg?: string;
}

// 定义基础URL常量
const BASE_URL = "http://127.0.0.1:8000/feedback";

export default class FeedbackService {
    /**
     * 创建反馈
     * @param user_id 用户ID
     * @param message 反馈内容
     * @returns Promise
     */
    static createFeedback(user_id: number, message: string): Promise<any> {
        const formData = new FormData();
        formData.append('user_id', user_id.toString());
        formData.append('message', message);

        return request({
            method: "post",
            url: `${BASE_URL}/create`,
            data: formData,
        });
    }

    /**
     * 获取所有反馈列表（管理员用）
     * @returns Promise<FeedbackListResponse>
     */
    static getAllFeedbacks(): Promise<FeedbackListResponse> {
        return request({
            method: "get",
            url: `${BASE_URL}/list`
        });
    }

    /**
     * 获取我的反馈列表
     * @param user_id 用户ID
     * @returns Promise<FeedbackListResponse>
     */
    static getMyFeedbacks(user_id: number): Promise<FeedbackListResponse> {
        return request({
            method: "get",
            url: `${BASE_URL}/my_feedback`,
            params: { user_id }
        });
    }

    /**
     * 处理反馈（管理员用）
     * @param feedback_id 反馈ID
     * @param solved 是否解决
     * @param reason 处理原因
     * @returns Promise
     */
    static handleFeedback(feedback_id: number, solved: boolean, reason: string): Promise<any> {
        const formData = new FormData();
        formData.append('id', feedback_id.toString());
        formData.append('solved', solved.toString());
        formData.append('reason', reason);

        return request({
            method: "post",
            url: `${BASE_URL}/handle`,
            data: formData,
        });
    }
}