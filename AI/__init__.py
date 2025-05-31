import asyncio

semaphore = asyncio.Semaphore(1)
autoComplete = None

def set_auto_complete(autoCompleteFunction):
    global autoComplete
    print("[set_auto_complete] Setting autoComplete function...")
    if not callable(autoCompleteFunction):
        raise ValueError("autoCompleteFunction must be a callable function.")
    autoComplete = autoCompleteFunction
    print("[set_auto_complete] autoComplete function set.")

def set_semaphore(value: int):
    global semaphore
    print(f"[set_semaphore] Setting semaphore value to {value}...")
    semaphore = asyncio.Semaphore(value)
    print("[set_semaphore] Semaphore set.")

async def get_data(systemPrompt: str, userPrompt) -> str:
    print("[get_data] Waiting to acquire semaphore...")
    async with semaphore:
        print("[get_data] Semaphore acquired.")
        if autoComplete is None:
            raise ValueError("AutoComplete client is not initialized. Please set it before calling get_data().")
        # Await if autoComplete is async, else call directly
        if asyncio.iscoroutinefunction(autoComplete):
            print("[get_data] Calling async autoComplete function...")
            response = await autoComplete(systemPrompt, userPrompt)
        else:
            print("[get_data] Calling sync autoComplete function...")
            response = autoComplete(systemPrompt, userPrompt)
        print("[get_data] Response received.")
        return response
