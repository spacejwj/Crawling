


class SimpleCollectKeyword:
    code = 0


    def __init__(self, code):
        self.code = code



    def Execute(self):
        #해당 코드의 알고리즘 파일 로드 (SimpleCollect_{code})
        #없으면 파일 생성.


        #마지막 저장 날짜 다음날부터 주가 변동폭 확인.
        #10분 단위로 주가 정보 얻어옴.

        #30분 단위로 주가 정보 얻어옴.

        #1시간 단위로 주가 정보 얻어옴.

        #정보가 많이쌓이면, 1달, 3달 주기도 가능.

        #==> 배열로 저장.

        ##
        #앞전 주가가 지금주가보다 떨어졌는지 올랐는지 구분. 해당 시간대에 기사 수집. 단어 분석.
        #단어분석은 올라갔을때의 단어와 내려갔을때의 단어가 겹치는 부분은 모두 제거.
        #남아있는 단어를 상대로 발생빈도에따라, 각각 점수를 매긴다. 올라간것은 +, 내려간것은 -

        # 그렇게 하루치 분석을 끝내면, 저장. -- 다음날 정보도 계속해서 수집.분석.

        a= 0

