const STORAGE_KEY = "openrouter_api_key"; // 고정된 이름

export const getOpenRouterKey = () => sessionStorage.getItem(STORAGE_KEY) || "";
export const setOpenRouterKey = (k) => sessionStorage.setItem(STORAGE_KEY, k);
export const clearOpenRouterKey = () => sessionStorage.removeItem(STORAGE_KEY);