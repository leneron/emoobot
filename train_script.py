from data_extract_script import Extracter


vkApi = Extracter()

# there could be less than 10 000 records, because vk has some limitations
# vkApi.extractNewsfeed('😆', 10000, 500)
# vkApi.extractNewsfeed('😊', 10000, 500)
# vkApi.extractNewsfeed('😐', 10000, 500)
# vkApi.extractNewsfeed('❤', 10000, 500)
# vkApi.extractNewsfeed('😒', 10000, 500)
# vkApi.extractNewsfeed('😭', 5000, 500)