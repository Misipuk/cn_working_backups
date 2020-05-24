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


login = "PizzaOwner"

userRequest = UserRequest()
#userRequest.register(login, "test")
at = userRequest.login(login, "lovepizza1")


#userRequest.get_users(at)
#userRequest.getCafes(at)
"""userRequest.add_cafe(at, {
    "owner": "AlexPan",
    "name": "Aleha",
    "des": "Aleha",
    "city": "Aleha",
})"""
#userRequest.getCafes(at)


#userRequest.add_cafe_media(at, 4, "D:\sem6_protocols\cn_client\photos\Tree.jpg")
userRequest.getCafeMedia(at, 1)
userRequest.delCafeMedia(at,1)
userRequest.getCafeMedia(at, 2)

#userRequest.getCafeReviews(at, 2)
#userRequest.delReview(at, 4, "Alex")
#userRequest.getCafeReviews(at, 2)
"""userRequest.add_cafe_review(at, {
    "owner": "Alex",
    "cafe_id": "2",
    "stars": "3",
    "description": "5",
})"""
#userRequest.getCafeReviews(at, 2)

