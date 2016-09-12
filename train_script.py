from data_extract_script import Extracter


vkApi = Extracter()

vkApi.extractNewsfeed('😆', 10000, 500)
vkApi.extractNewsfeed('😊', 10000, 500)
vkApi.extractNewsfeed('😐', 10000, 500)
vkApi.extractNewsfeed('❤', 10000, 500)
vkApi.extractNewsfeed('😒', 10000, 500)
vkApi.extractNewsfeed('😭', 10000, 500)