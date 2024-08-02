import toast from "react-hot-toast";

export const sendPostRequest = async ({
  url,
  data,
  baseUrl = "http://127.0.0.1:8000",
}: {
  url: string;
  data: object;
  baseUrl?: string;
}) => {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };
  try {
    const response = await fetch(baseUrl + url, requestOptions);
    if (response.status >= 400) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    toast.error(`Something went wrong. Error: ${error}`);
  }
};
