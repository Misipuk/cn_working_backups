import datetime
from typing import Dict, Optional, List


class Review:
    id: int
    owner: str  # ownerlogin
    cafeid: int
    stars: int
    time: str
    description: str  # login, review

    def __init__(self, owner: str, cafeid: int, stars: int, time: str, desc: str):
        self.id = None
        self.owner = owner
        self.cafeid = cafeid
        self.time = time
        self.stars = stars
        self.description = desc

    def copy(self):
        r = Review(self.owner, self.cafeid, self.stars, self.time, self.description)
        r.id = self.id
        return r


def now() -> str:
    return str(datetime.datetime.now())


class Reviews:
    # cafe_id -> Reviews
    _cafe_reviews: Dict[int, List[Review]]
    # user_login -> UserReviews
    _login_reviews: Dict[str, List[Review]]
    _all_reviews = List[Review]

    def __init__(self):
        self._cafe_reviews = {}
        self._login_reviews = {}
        self._all_reviews = []


    def get_by_cafe(self, cid: int) -> Optional[List[Review]]:
        rvs = self._cafe_reviews.get(cid)
        return Reviews._copy_if_none(rvs) if rvs is not None else None

    def get_by_login(self, login: str) -> Optional[List[Review]]:
        rvs = self._login_reviews.get(login)
        return Reviews._copy_if_none(rvs) if rvs is not None else None

    def put(self, review: Review) -> int:
        if review.id is None:
            if len(self._all_reviews) != 0:
                review.id = len(self._all_reviews) + 1
            else:
                review.id = 1

        # To list
        if len(self._all_reviews) != 0:
            self._all_reviews.append(review)
        else:
            self._all_reviews = [review]

        # To dict
        if self._cafe_reviews.get(review.cafeid) is not None:
            self._cafe_reviews[review.cafeid] = self._cafe_reviews[review.cafeid] + [review]
        else:
            self._cafe_reviews[review.cafeid] = [review]

        if self._login_reviews.get(review.owner) is not None:
            self._login_reviews[review.owner] = self._login_reviews[review.owner] + [review]
        else:
            self._login_reviews[review.owner] = [review]
        return review.id

    def del_by_userlogin(self, login: str, revid: int):
            cafeid = -1
            try:
                for rev in self._all_reviews:
                    if rev.id == revid and rev.owner == login:
                        cafeid = rev.cafeid
                        self._all_reviews.remove(rev)

                cl = self._cafe_reviews.get(cafeid)  # QUESTION
                for rev in cl:
                    if rev.id == revid and rev.owner == login:
                        cl.remove(rev)
                c2 = self._login_reviews.get(login)
                for rev in c2:
                    if rev.id == revid and rev.owner == login:
                        c2.remove(rev)

                return 1
            except Exception as e:
                return -1
            else:
                return -1

    @staticmethod
    def _copy_if_none(rvs: List[Review]):
        if rvs is not None:
            rvs1 = []
            for r in rvs:
                rvs1.append(r.copy())
            return rvs1
        else:
            return None
