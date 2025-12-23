import axios from 'axios';

const API_BASE_URL = 'https://api.example.com/chat';

export const sendMessageToAI = async (userMessage) => {
    try {
        const response = await axios.post(API_URL, {
            message: userMessage
        });

        // 백엔드에서 준 응답 텍스트 반환
        return response.data.response;

    } catch (error) {
        console.error("AI 통신 에러:", error);
        return "죄송합니다. 서버와 연결할 수 없습니다.";
    }
};