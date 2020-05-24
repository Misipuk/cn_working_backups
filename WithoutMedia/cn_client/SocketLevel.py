import datetime

from UserRequestsFile import UserRequest

# User
# get users vverhu
# get cafes
# post review
# create cafe

# CafeOwner
# UserFunctions
# Edit functions
# MultiThreading


login = "PanAleha"

userRequest = UserRequest()
#userRequest.register(login, "test")
at = userRequest.login(login, "loveAleha1")


#userRequest.get_users(at)
userRequest.getCafes(at)
userRequest.add_cafe(at, {
    "owner": "AlexPan",
    "name": "Aleha",
    "des": "Aleha",
    "city": "Aleha",
})
userRequest.getCafes(at)


userRequest.add_cafe_media(at, 4, "D:\sem6_protocols\cn_client\photos\Tree.jpg")


#userRequest.getCafeReviews(at, 1)
#userRequest.delReview(at, 2, "Alex")
#userRequest.getCafeReviews(at, 2)
"""userRequest.add_cafe_review(at, {
    "owner": "Alex",
    "cafe_id": "2",
    "stars": "3",
    "description": "5",
})"""
#userRequest.getCafeReviews(at, 2)

