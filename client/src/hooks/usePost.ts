export const usePost = (baseUrl: string = "http://127.0.0.1:8000") => {
  return async (url: string, data: object) => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    const resp = await fetch(baseUrl + url, requestOptions);
    if (!resp.ok) {
      throw new Error(`HTTP error! status: ${resp.status}`);
    }
    return await resp.json();
  };
};
