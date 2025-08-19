import time
import pyautogui as pg


def wait_and_find_element(image_path: str, timeout=15, interval=0.1, confidence=0.7, is_multiple: bool = False):
    """
    Waits for a specific image to appear on the screen.

    Args:
        image_path (str): The path to the image file to search for.
        timeout (int): The maximum time in seconds to wait for the image.
        interval (float): The time in seconds to wait between checks.
        confidence (float): The confidence level for image matching.
        is_multiple (bool): If True, returns all matching locations.

    Returns:
        For single image: tuple (left, top, width, height) or None
        For multiple images: list of tuples [(left, top, width, height), ...] or empty list
    """
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        try:
            if is_multiple:
                # 모든 일치하는 이미지 위치 찾기
                locations = list(pg.locateAllOnScreen(image_path, confidence=confidence))
                if locations:
                    # print(f"Multiple images found ({len(locations)}): {locations}")
                    return locations
            else:
                # 첫 번째 일치하는 이미지만 찾기
                location = pg.locateOnScreen(image_path, confidence=confidence)
                if location:
                    # print(f"Image found: {location}")
                    return location
                    
        except pg.ImageNotFoundException:
            continue  # Image not found yet, continue waiting
        time.sleep(interval)
    
    if is_multiple:
        print("No images found within the timeout period.")
        return []
    else:
        print("Image not found within the timeout period.")
        print(f'Fail image: {image_path}')   # Print only the image file name
        return None
    

def find_and_click(image_path: str, timeout=15, confidence=0.7, is_multiple: bool = False, duration: int = 0):
    try:
        element = wait_and_find_element(
            image_path,
            timeout=timeout,
            confidence=confidence,
            is_multiple=is_multiple)
        
        if (duration > 0):
            pg.moveTo(element, duration=duration)

        pg.click(element)

    except Exception as e:
        print(f"{image_path} 요소를 찾을 수 없습니다:", e)