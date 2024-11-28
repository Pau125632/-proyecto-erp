#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

logo_path ="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAO8AAADTCAMAAABeFrRdAAAA0lBMVEX///+Sa6zJq9GKX6f4+PePZqqNYqjo5un+//2NYqrz8/OrlrvUzdv19fX7/PqRaq2OaKfi4OXu7e6IW6PPxdiyn8Hc2N/W0NzBr87Jp9LDo8vs6uyNYKrJrNHXzNrf1+HJtM/Eoc2+scjm4OjDqsrNvNLLt9C1o8KiibWRbaiEVqO8rcemjbiVdausmLvY09zHv8qdgLHGu82Ud6jRu9fUxNm+ocTGv8jQy9G6qr60pbjc0OG8nMT18faBVJ7Atsipjr+klbCDUaSdiqu8tcHDnM7IhamGAAAevklEQVR4nO19C3uqSLY2AlVcVBBECBcBFVRUNJDW2TPp7nyz55v//5dOFRcF5Ja909mmz1nPk2hMifXWuq9ahQTxoSSRJDmf2/THXvVxKdbJhNRfPZFPonWGV1+Pf/VUPoXmczKn/w0sNvUr3LmhsL96On85qWSBdPdvL9OviXnGv5KfOfOrJ/QXk0LqNivwHulLBgZs/M2V2CdJEz3YpLsWElNtaL96Sn8puaQhoAf+IqxdwjYwh+2PubLwMZf5YHLJS/LoEcTZJxgPsVj/AMCC4xqXR7QFru4mj76MfjSCXhsfAJi2PWzu3Z+d3F9A7txTEVTCdtAvD6myhgH/lA7TtqEb2Np7HzPFDyVX98en5xOxekV/8B5SOhPx5mestGP4lzPtknN9/WGz/DjydR/9lp/VRIYd/IewJueLH9U9xpszPkOssB1wPmyWH0fnjAt2KnzrFf6tLci5/CNXY8+GQ/yDEM4G1uAfusRfTApppKmvkzCY9pK/mLnu/YA/YS6+QHwjNP/NF0jyEdWXcEhdSZ8lFiuVaITbXfjvvpZtIOn4Ji1XsseiPET5uFl+HKkoLZLSp24if26muf7inV5JcF0kG6d/omXzGELV9Ud0v4SJPIdhJk/lJ/ybz8Uw/u+7JiyTZ/T7GXuyM+KsonsPmVzyBkqMMg5ridu1c776xjuyQ/OC+Ko+Y6Vf4XXz9PPHTvSjCNlRnVysefw8SX9ZL6/duf0d6MpgCCFOlk2+jPEyGg8pzkn9ylXV8+82Ys3Yxa9IuaWie+dKjsETcpys0xiHzciFP6R1RmTrOmYL410clnASm/rE8+n/nAXf6xoOYqn5nDylPQ3/0j8i6fhLSNLJVPJU76IJr3iarxeUFCZIvV5cWl1owkzxCZ6NTZ5EGo8YbGAa6+QqfcY6nuF7vkCvSUM5X85IDaVFD4lmkF3jvyVPBRfpwh9r0yUfMXZOyS1YUsZHqY2hk1gmcWhIuN18ki/InaXCzLouusabjRIk6S+b78/SWS8KLa0+6XM9ASl7a5bpTHIELB7/SJ/iiMO5fBujIOYvmuwHkKSXecie9Zw757lP6h2p4Rop7LdE2WkPrU2MrB5yvg9cBBPu6hm+vkxBCoY+J+etW2k2wmgmo2nP57UYIz/p5CNvv93xkPX8cZzEmN6zfs0nasm8CJnyyp7xZieCwl9a3/LLSdLnlcBCRShO2OJ6jGTk4XUdsSgzIL4JSQ1nnvlq1iWNfm77F5Hgkd6ltJMiL5AN+iNGrJdQotNSd1POWJpXZ3dxlRF6/aCZ4I0UXULep6jEHnZR9JvgaMkORAaF9XO5X6WDUZ6LAjPDUxzGd9P/qHMkLQ/NXsShBZJY3veca0lDMXAyR8cy9kZrfZ7+AyUB2QjnNXl4cuR1FoklabOsuXqHwj8EuUlpQ0YxVcYZKWXpOF4SSTSc8V44Z47KSR4d3Vgo6QrQe0LQvIvvrBT9PWnkr6FVFnHQ9sVNmDw23OQF5oIXgDFyCZUy4D72N4Kne7nn1uaK4a6wUNgPmynciPVyxRQk1/BXskRm1Rg7EVxFz1LEcRZtYbYTmr7OFeBs6B6TXYp8zI2jEjmLmwemHRdF0LlRTpCxXu6T9kmRZpyYs0wGEPkq6WfVG3XxiFXnKgleyTyPUcCfxZRpnscsMsamTS0rjMle5H7ZX9lu9pS/LcJDk6PrbrEAQ/v5xJ8T1T1n8O0kd1SSik1uhpVTnEfgyDk9at5bJtabX21tSnYm4nSc/L6k5ca0Ko+Zfb5ko5V/OUzCfeaMFOHhfVFGksE7pKEVEPuZs31NOKsuTvjBxJorI9DjRVYliNEqYVu18hZI6x+zCFtHroL3Quc3a8NnKi0kJotYJ0HHGBvqVySz51Sh5Tc+2ZNYPRnr19X6UYuSNcRjE4zC/ouT53JnPTVIr8kamMl+A4vxxriokYxSsLDTnuatGcRY+gu43htpSU2C1kjDlxJJVnU3ASVkW4dJ3PSGsCLJXqM1EOxlItP+wk0XZv11pBmTl3GHORsL72yrPknuv2EkKYOZBdZdhFejCRMtgRanwusYp/R9py9im3OSf8+1j2VekanV5yRpqs9jJLAJ3zwcVb4l6b0rnZ6zKNm8ZE+YxVdr3XKMQhmGlRRPJz2BsDUiqUoTqwUyabEpMcgWx3msIV/S0Jo9LUafPd+fJt8tKaCAJNtFOH0+2VJCUeVYnusbXO/Jh/DYFZmva9f7gf3iX04FIBnx+BXaj5MStaNrtj7Xefs6Sp4rpjY3PJ/UvyBc7Fqq8ZGAAQtuki+gIEvBbdJ5ZEWsDEO/nFc0wXxNuAjSXe2JJn0BoU580lkn56T7lCX99NnwbLwOY/8rCnNKY29dcaKS7pnpPhhhIu56cYqN1YxzYs9p5Z+LrxI139NY+t1T5WLiIOukodBJ+HXCDbSJc+JtI03wmWfN9h53s6idWMe7+K+KYXju2ZFMmed52UFeaa6TSuzxaS+8NjYdd0GiGIRXv30zZdd/5M2ENpK9jGeu8U8f5Ye6bpB6cr4BPcOFx+SUg47I+Ofp27dvKo9U1/s6KUKF5FuNwyFdlZdX2tnHdFYcabXy80MOF18y/0iCKuk37ytUb+pJIF3DT5klCChRMny1JKisl3BXkVJ7Rktn77evqriYzj7BO2c/jmPfjxXbcWz39/naVmWZF1iaSVuaSY//w1Qd28c1va+U/d3RuGYXRGCcV2+xWBgXA++MkrkqI4PmIW3O8sWvSZpb96rpu+eVPOb5ccpe0jPQDy4JjE/GXI8/eZIfSK7DlgrlrCAzmuvnKa1gJOeUnghpnm+AO/qDb3y2ETsnjYu3XubkepuLXihHYd/7RmKVZfK6s4Ryh6+W8l6JNzynoo3apcA9V9eVddqn4Gab47ZOfl2TJRtV26MW6xUSSv1lMmmBzTVdwAbsy+L941L+m+UvhTYlHjlexpkbScewdOGRpsvuox5R6EUFvGMG1yvmt+IqCj5iFHu5+sjDYZWpLy6ui5wUST5mT3cf+sNIH2XbM7yzY37TybS4wzLniy97LkruPWGOTRVvMKZpymPaI++U4MsQj6fOa97iScU8POsXXfcc59W9eDZPrMkx4ekekewTj3NRsPWnXzjjnyOa5GXfMJTE3wquIbHMybYv6xW20QpOfn1DJZL0YJwbMu29RxweiTx3kTesjL2ntKaspaUMO9kbE9BryfaSmW96Kl9XffF2Sb4dyl+yks7KTR5Oty37BK/jOPiwAsHMv9b+SZns3P3IRt6skR650hanfAyb+Nu1hJuXXs8fcnD2lxGTCal5yWuN6Xkk+wYXpchzAVk2zFzB0x+3h70PCSlOycjrk6t0/7MYZdHGmyu5aUs0irget4e9D/nYCGuLHO4YK6fsGcUSxtiQ7YWvLTBfZVJv7iP9CsToLr++HZNcv+L9fq8ksjySYHzYFS9Fd+f74xFbSl89FCRfM0BnQcvuYl2On3iU7+K9beWJ4d3FF9LeseLvh4dw8mex1dFB+U6+USBcPEW/68rHePGZdwEtzJfpxME01pYAigNxWuQfi0xuVjtnY5QLeHf6iYPOpHdBIUnvi4XO41AUByW8hIpPKyiO6vgIrWHf90GOEd7fsMQzuvEwpVhtNttgmr21j1O5SQUv4evzebqLoK/rtFMgaULB3ld+pB0yOQAAgt2pa1xQ5S/udE5q6obXUJfyeMLBNQ7bfaRIUuEGA3DsHDYDVbzE2MebQ57ahAaFXNKFJU6P1dItQYR32TnsDd7hxacv1JYw4nVF8AtFazmx8itoBQdiD7waV4O3nU4ODpwfx1alpFniAG46h6nvx2u6xJh8NLjEPjiKYtQ5TK2T5w4yVP/h4BIvS4kaUJ1QGOr9eNXf76OQX038TiZCEXa2u/0IXuKR/FBGywNBxFDcdo37IbwPSBMUaYyBCLsE72+C9zTBv4cA7DsGduOl5ZU2UpSRtpJbB/KMs7p/aWSPbGcltx9HYnnJsW175DA/urV6SDwvcjaTDl1rx8vEw4DaTUEQhAHc7WC4GdXN6Pm4DQMArWHhNXo0Q2/NiAIv+1PDx5jxYZKPm1LBIf6B+i6/S6cVilyHxWrBKy/D3S7aayadrJkwlpQh2E0j5W48bcYUSizB7HbZIfwOD3vFWa2Y1Sg+hlPLmmxqkIyi3S4YLpEMrFbOaH+YWBYVxu89nYatFaaY67JYjXjNI7UL76GdDhSa+H3kLKFM+op3fNzBWTnb4OMQctSx8kYp3AXL8ipIGwDh5J09EiD7MAEOqHbxaMArbCjrpT4/MocUrAlUj/CK9wSm+5pcQpkAOCldc78LalJKfkOJ1PY9yUhqrZJZANAeU9bjZRAzmpf4FAAuquqxauV4411U7xXoAwrmnq9/stvdrF5wVaQbwTsqY9F1rpI1mLQqQy1eDYJBW8CIJg7EygAaZPobf5/VvSehIzeh8noYG+0a6wV8IIpBbw7L09vQSORaNzzq8I4sMez4sCMUQUXcwxSvtmtzgUMk9Rnzh9OW+3PwkwHoDv4z2hfS/Bi2v68Gr0oNJp1+cMiJoCy1UYKXp4YN70hICESQWlDle6vnOFkD2NNoCVAq/iHCNtG8xyuDAdUj+9mCQVh64ZDg3QbtDv+EkhjMV37akasegTjpF/hpQfGvTbvFuse77Q7KMMloIUvjkGmcEafv1RirSpGYuMhjVyBkcoMWk1m6YskMMEjTWizWHd4RJYZNg0uEfDtVtKEJ3qizYqZx2EXKu87MDclLLw02K0lvBGBL3fQObyDCfvf5YdHIouRg18fsOr0IOxnAJbHvXlMNrWefNHtTEV8Fgpfm0VW8ijXox17M4IFYeCvGu2k1VikNgXggJt2l6zEYdAXDmFiuElAJQOSa7U8V74vY1ywSNFWKzlEythn0aKVUoBhIfXLQqE/9jRjdsWcDQXMEUMHLwAHsnZMhD1SYEOLby6BH5UPlxMGxhxwQMywI3ZO4kxSGEkFj+FDBuwTdJZEr7WHRtA3BAPSBIePCeJ9jlUvYw3IyNcY4apHRCt4tgN0165xG3ADeGIrwthnGKyG9HMA+wbHNiZPOQbMa3znimheqjJeGgxZdr5LEDayb8CO8VdNRS8IExcZ9Lo+WsxOvUFewYici1WRIynglagD7V7P+QLHS7eOOiL998nSMt4deJg6pE69S66L3oHHnrIx3VFSZsaRpJ6YFPlPCi+xVL0+G8HbkqBn1wRvWxgomYluDxSrjXUKQm6vRFlAQchyI4iZlUyvy3M/UCZM++3hEL7wMqH8dmaEGi1XGOwOZiZVCDoiiiH8GkBrW6zTypIUJDUEv84zxcr02ynvgrbNW2VsbZK2Mdyumgo+CaJGDwfawDQGHAnBrWBfZzUoIh6DFzRcIyXP3tkc26Q68NNUQK6Cglau3WHd4sWqhDBgE2d0IBCk+QET7e1s0Ea1C/8AvwKvkCkTzJsMw8vjqHfewwWKV8aYRE5I461iExysvFhVUJzmySvuPvwBv6OA7SAxD8OeOQjT9889JNIxXCI/cFGPd4T3ixYF3esHM4C4q5bZ0IJZqn5+PVwqYGYDR3l7JtMCyrECbq9H+EMBoKR8AV2sU7+R5iCYE6gzt+C3YRaPrWD4E5cTx8/HOqGAv1UTsvLMJmoKaKl7kUzQIG+IkZzidHvwTY8qnDbTCstX+dLw01XIZGUlfXXNS1R+hVdnD5vCHHs3C6Z+73Q4cqp7+0/HGre4eZRt1MKrxBoonh1b7dGhTYuR7Mfp0vHcGtETIYtVlJZV4EmU86rZXGeWOPhvvqsN4D2tTvTJe9BfY/z/wQxvgn4332FFFPVmDGotVxos8rxgNu7POOvpkvPy0K4dGFus+m7jL9weDl3fgLbz1k/HGncXafZ3FquCNcUN0/woWsS/mR5+KN+isGssoXb2TgQpeXFxqCrXr6D+3p5+LV4LdpcFDTUNltR6LBbp/CcssIPxcvIceez7YYlVXpYpXtQaDHm2IGQ0LQvWpeOVpH58Z3Lev3O2nROJg0Fjtqr65WLD6VLyzXqWjPRxUYzDGquCV3sHgl6JQfSZec9dL5eRSgS0hqYqX2HODnjuRs2kxxfxMvAerX9U4EqtzUuGgWhSJwGDSEUIntC8v8qE33l77YEnZvGGTWKN6Vo0Vrro9dOIGVsVJ8QEQB1RnSW1DlXUoEvvV68Y99yEIm2sohtOTnlvUBA8GldpvDAdWdUtenoCBSA1bW1bMiAPldQr7tJcTiYvvV49dggFXG/kcem2kZZOqbJhs6lZbDvHhlknc6NLpPQQVI04Dscd2D5FUrfsJ/hHURz5Lrt/GHKatKIovRRiRWPfpwpFCbsmaLGu9HLMBAEwqFmNFDbp6+bLpIuHpJY6IN7DmuJiPPqivPCO8KHwqVCqT+LGuI00LODwURstTSabk0z6EQITbqqRt8DZnn0aXUOy3MBKSsZpegyWecb8NRtz+hAeD4RXgEAyaphkHFsBNrxAG0XGzR7QZRgHFwYFohXcG1sQXGky6p/GMYfTZecGBj1jVtXiy4zBZYefJObRiCEI6Gh6Taro8tAAmqq69E/H4ACGGLIogI/wUWtG9O9EmMBkQdEyDfqPST6zdsCiQvM2m9laaGmPKsol+0K/29yfXYOSMTJMZE+a/h7Ocjptayz/W9tGE4jiI0eDdMxgelXsePh+vFxoen2uuk9O/jvlHDod13dBXWLepHY//+tzv6hBMdRQvkTj7iib94iODwthU7bdfPIl3k/SjN8XmN4EFYXeP14PRdtfL/9YSMrD3RYsHJxP2aUitJ37y9fASUZ9Gsgbail8P74xr6XDsoCdQzW8en5awV0NSLSnw6/HXhz9W0sdkc18P78/wd/QF+Ttr61DuoK+IN+R+3D5/QbwmV7OR1ZeqeFG4+/r66kjde0A0ozqIpO7lGpuSgy76qtbtc7+fjrBvul5DRbxjbTaZgjCKohDuptGyOYrhR8MJFWwPs+MhAtOXfeOpEl7bvMBpEB1QwjKMQjANhtUEyfz34TAc/qcpipf+jf47LNQYNOqa7kvJW4fDw7CurTf916GcH93wyrMp2DtZzxXLOxuwC+vPlknD6WQp5Rkgayov34Nl3alJJaJ2ob+6/QtfdvJn9cCq/ALBtFmgGJRNXh2QsKSiwoLJR5znBrVvXlIAZd6VElaOl958j6paMQp3wX3Fix9+j6q3uGUOO3BXY48n1vRYk1er2x0oF5Y6jgHcKudKEARhFAQvYRgGqdHaw4FYX34zqYF4txIZXiaY1hV19xZVlZQTmNbtHpxA5QzqeGuBoEEjTsAKS1IdgTa8wqTUDCVRpRpp1NQPzVPi5G65U7ynacP50RNVOdAXT6snO/Orv1jFa9ABEKPGysIIQFCsT2xa8RJbUMSrlvGalBjWmkGGqtl4SfCq08YDnSoFi9mmQjU23bMhVziDekC607xpIcAIFA9VxrAV7xEUA8gKXvTf+ga3k1Uj5xgvD0Dzp8VUYW/EpGq7zlLiJ/BaN2So1oNI0s4sdR0q7XifYBlvOf9lYH2v45KqYSLCOz60HaXFG1nXuURc2wE/DVrX7wPlWmu82wkaQd2s3k/hrYj7laK6OvEIgudp63YKWr48fFO4FkFIPzjTpGdr0HwclT/sRoQQFFqMfw6vZtXtsPO1h9BGcBA09XdmNLwak6DjpMTJsrT8w7imq8p7mPiCYUEpUVb6E3iJSZ2FjmtFEeFt6e9Mr89lqqhaXSeEbjxjhtuqcWTpsTTahLtpWiyPCxh/Eu+Sq1GesHauGG9XfTPIdiqPXFfgerzPTPlTfNxGwSSYiDBpjM3Pq4y4W2XlJ/Ga8L4nSKqfK8Lb2e+4ySxWwHVtaCGelfcvnsLddyo8zPbrtR8r2qrAhtPH4UU29W6dZ/Wb4qMeN30ageRghcxxXXmYzRUbPFDguIt8piHq0D4Q78mqTk1o4CKyz527kAxMFBi5m0wlBJ7nay+HvNtNa45Tatai72W8P2OfCWw4KkbIbnCcIwi77yieeiQUBCUgpeMEQm4SLe9tRKH6R0dW0HrzgdNH4t1DrjybqCF0H0Gu65YIBJuu3oZL+l2OyTk5yoLw/hjV5upj2AiG7XbhQ/HKlTMxcpNlRRLYvRUaJYHiLIkm/sNZUaxK0mm5hdS0cozq5Rp/ocXpKHxo1gfiRRar1Hy0aQpmkTx3F2SiJNY9Yrxv1u1wNa1sd6UddPVaejCtzqahD9VfbLEKbpVtDO7ehXdC0JW+Gmazu50pFUIrd4Ob+pC2SM8c94F4kcUq+BmtsQEH6W9380eYXAslqYRydzsfIQ4n+xMvCGMtmOZw6Un3llYMPxTvsghk29ixOoLdvYS5vQIUP6xrWWOWEaQgBW7eR+KszoaQDeCulqMD7wZ045ULjpVvFi4kz93deTDJExTIqWFTrE2Pi5bL7rGKW7E33kOlvlG7/zu8Wax9cwPeCHafDmeo5ISxQ4Fl0KdFCu9otcZLmIRAvAlgB96wB39x2SOPJOrrlQmheLKzbVFJjRQPQBT2u3vKnqurLZRoBQdWAW+bV6QnYg+8yGJlSJyWhK9PvjDL8oVQHEw6buhO0MnF1t1efV/Ga7VYTZUTe8gzslhZyj1ssR198sFJJgJoip3CryR8RRLRYa8E+J8CXqRVLVZkD3vh5bNCDN3mCjF/OxKkE5fdIECmBmLXTmS6HqrV1bMbQxRPXvEyXFvWMjn00d+kRR4bzbjNxiC8Lx229AByiT+AQccddFfpZ427bqZBg83KuuFl21qwR6EPy/xtuMWcaiX1wrAtgEKS9I1qZbAEr7EDvn9Ke+9T/lkHYLXmysOpoBbwovHNaUvg/wbb6s+FT8cWS2q1vyOOoofNd3IkcDB5C0Y33MBqO2xzvWHXyZoELX2LS/SJRXlG02jUqv30Lr5qOsEWc4jzs9aFVjiKR9Ffs5QuYWF3mQ3BoOXOnf6tVy8C1Qy8eM3dMckHC2wK7np3M9K+xwhv8UYoTGOdhcfBRPud/GJo8SigaEzeRlSpaDUOQfMN6ma7m3eWJwPuUM9hdrbDvCzj1axBrVaOplscP1OFl2TYuHWBUppWa4VDU5yVqbDaX59/HLTKHmgcIpEe1q3OKdwVh6qUCMI6udPC3Raz4MSVAM64Ose4n2JlegJFd85OGs8f4K9HaDeoUdpvJod1R67oze7u6BR7tAaAG57KUjNWXqxp+QrSBIhUpFW+7UkJrWnKgVNFLIeWSB1Kqy4ogZWEhk/leyQOU4dRF8GFHc5Vgln/JLvcBaMyBmE52UU1Yc8ptADggmF8kmR+zJuSso8gRwXVTXDhaAGRmxyWI8bkaTTueY9W18orSyeuErwsKQCoaKkmsZzAjGYTyzoky/VUNgZaomPsv2rwxK03pmSZAILcxoz3k+lQSe/GzdKMMpz+uW0Ikk5bwCX96vg2LJbFQQhrA2tmNuEggJxFpQMtChyuIq7tAKWVNNwcQnRZi0JvgWg4ZUXZ5z9RwNoXj5EjF6m81PGXb7tnGP+WnKO4vo9V99GUEoMwANR0ctdYUnrraPOCgHAcRjvZNra20Nr+ZYJHoXEgnNmFxIXBRziW/780XFaGAUyGcyDaXy+q4aH7f1yHCQdqVx9VjN7dGp3cKohpv5f+dagkSUhWO4axMsOgcR032S9OQGK6RvMNvKjfNPrb0qr3Ueu/BzXcM/7vSqP/XeylOzbu+5J56tv2SKutdo5pLAKo+TcgnH7iq4K2P942WyLN6DtS/m/rdO1L45e4/ZY+0ov3tb4qBbc/7NMFLkjyNS6StJs8CI7DS5lPuOJlVqtr4yzvrPg7r6tev/lWGhPmnXS9erJ2e4+wcq5eZZ3jNa54C7ORV6tV/ofgqPy1d3O1u5YJhGGve0zIupF/R6uvu8Y5f7e3II1Fhu2K94nUjew1xkBEVpwk6+mX9CV64RBnj6jQK2lcrt+ySHuGZ+RrfeXv9RVf967fHmsbZL6QaGKGscjBx3nrFTsaTHsdSuKvXygtLb7J3/IrnQyTVfJvCLziFXgjH+3PecGdV8XTzN+f4HXv8BoMO8q/E9Y2VDk2hAa8jP7NvM6GFdz8Ws6CYe0r3hE1gOHe94+B1ZDg3ePNF9Qh58aczJYxnmMW/lHBSyhkjtBDkqBV+UvIC/M27xq8Hv5q72yya5I05he5ijeTZ0efG6SR27dVfl1CueBPyfHi+oMIUGBLDXvedOuGV0JXMXOFOqEPsO/4e2Ufmq1Hs+68ite8zguJ7ZUnN7yGRNhX/pI0cT0wes/fhUTI+WxYL9czwkHLdeMvwR8gykIms94H7OTbF8X7C2+Ra4zgIjW58neRcRWp5++ZAPB1+kuYV/tsL35f3E3i1TB+X+QaQXuLy3/z7O3ePiuLyyIvVdiLef4N6Kxb1F/8DhRr98SaEHNLq5hVwT5LKz7/a5w/wZlEPny8YuQ7A0zf7n8sOffmkmfk8kdch1zPW9+mwzjXm0MmGUz2nMUT+xt8Zdr/0QfS/wDylpBKFqZZegAAAABJRU5ErkJggg==

# Configuración inicial
st.set_page_config(page_title="Módulos del ERP", layout="wide",page_icon=logo_path)
# Ruta del archivo de imagen (logo)

# Mostrar el logo en la parte superior de la aplicación
st.image(logo_path, width=200)  # Puedes ajustar el tamaño cambiando el valor de 'width'

# Agregar un título o contenido a la aplicación
st.title("Sistema ERP")
st.write("Bienvenido al sistema ERP para la gestión de clientes, inventarios, facturación, reportes y análisis de ventas.")

st.sidebar.title("ERP_ITM")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo_seleccionado" not in st.session_state:
    st.session_state["modulo_seleccionado"] = None

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Inicialización de DataFrames
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Cantidad", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])
    
# Función de autenticación
with st.sidebar:
    st.title("Módulos ERP")
if not st.session_state["auth"]:
    st.sidebar.subheader("Iniciar Sesión")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario == USER and contraseña == PASSWORD:
            st.session_state["auth"] = True
            st.sidebar.success("Inicio de sesión exitoso.")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
else:
    st.sidebar.subheader(f"Bienvenido, {USER}")
    st.session_state["modulo_seleccionado"] = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Generar Reportes", "Análisis de Ventas"],
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["auth"] = False
        st.session_state["modulo_seleccionado"] = None
        st.sidebar.success("Sesión cerrada correctamente.")


# Funciones auxiliares
def exportar_csv(df, nombre_archivo):
    """Permite exportar un DataFrame como archivo CSV."""
    st.download_button(
        label="Exportar Datos",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/csv",
    )

# Funciones de los módulos
def gestion_clientes():
    st.header("Gestión de Clientes")
    
    # Registro de nuevo cliente
    with st.form("Registro de Cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        
        if submitted:
            # Generación de ID para el nuevo cliente
            cliente_id = st.session_state["id_cliente"]
            nuevo_cliente = pd.DataFrame([{
                "ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono
            }])
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], nuevo_cliente], ignore_index=True)
            st.session_state["id_cliente"] += 1  # Incrementar el ID para el siguiente cliente
            st.success(f"Cliente {nombre} registrado correctamente con ID: {cliente_id}.")
    
    # Búsqueda de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Edición de cliente
    cliente_a_editar = st.selectbox("Seleccionar cliente para editar", st.session_state["clientes"]["ID"])
    cliente_data = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_a_editar]
    if cliente_data.empty:
        st.warning("Cliente no encontrado.")
    else:
        with st.form("Editar Cliente"):
            nombre_edit = st.text_input("Nuevo Nombre", cliente_data["Nombre"].values[0])
            correo_edit = st.text_input("Nuevo Correo", cliente_data["Correo"].values[0])
            telefono_edit = st.text_input("Nuevo Teléfono", cliente_data["Teléfono"].values[0])
            submitted_edit = st.form_submit_button("Actualizar Cliente")
            
            if submitted_edit:
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Nombre"] = nombre_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Correo"] = correo_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Teléfono"] = telefono_edit
                st.success(f"Cliente con ID {cliente_a_editar} actualizado.")

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

def gestion_inventario():

    st.header("Gestión de Inventario")
    
    # Registro de producto
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            # Generación de ID para el nuevo producto
            producto_id = st.session_state["id_producto"]
            nuevo_producto = pd.DataFrame([{
                "ID": producto_id, "Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario
            }])
            st.session_state["productos"] = pd.concat([st.session_state["productos"], nuevo_producto], ignore_index=True)
            st.session_state["id_producto"] += 1  # Incrementar el ID para el siguiente producto
            st.success(f"Producto {producto} registrado correctamente con ID: {producto_id}.")
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["productos"][st.session_state["productos"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["productos"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["productos"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"][st.session_state["productos"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes antes de crear una factura.")
        return
    
    if st.session_state["productos"].empty:
        st.warning("No hay productos en el inventario. Por favor, registra productos antes de crear una factura.")
        return
    
    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"].loc[
        st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
    ].values[0]
    
    # Selección de productos
    productos_seleccionados = st.multiselect(
        "Selecciona productos", 
        st.session_state["productos"]["Producto"].values
    )
    
    if not productos_seleccionados:
        st.info("Selecciona al menos un producto para generar una factura.")
        return
    
    productos_detalle = []
    total = 0
    
    for producto in productos_seleccionados:
        producto_info = st.session_state["productos"].loc[
            st.session_state["productos"]["Producto"] == producto
        ]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        stock_disponible = producto_info["Cantidad"].values[0]
        
        # Selección de cantidad
        cantidad = st.number_input(
            f"Cantidad de {producto} (Disponible: {stock_disponible})", 
            min_value=1, 
            max_value=stock_disponible, 
            step=1
        )
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        productos_detalle.append({
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": subtotal
        })
    
    # Calcular IVA y total final
    iva = total * 0.16
    total_con_iva = total + iva
    
    # Mostrar resumen
    st.subheader("Resumen de Factura")
    st.table(pd.DataFrame(productos_detalle))
    st.write(f"Subtotal: ${total:,.2f}")
    st.write(f"IVA (16%): ${iva:,.2f}")
    st.write(f"Total: ${total_con_iva:,.2f}")
    
    # Confirmación y registro de factura
    if st.button("Confirmar y Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        
        # Registrar factura
        factura = pd.DataFrame([{
            "Factura ID": factura_id, 
            "Cliente ID": cliente_id, 
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, 
            "Total": total, 
            "IVA": iva, 
            "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura
        
        # Reducir inventario
        for detalle in productos_detalle:
            producto = detalle["Producto"]
            cantidad = detalle["Cantidad"]
            st.session_state["productos"].loc[
                st.session_state["productos"]["Producto"] == producto, "Cantidad"
            ] -= cantidad
        
        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total con IVA: ${total_con_iva:,.2f}")
        
        # Exportar factura
        exportar_csv(st.session_state["facturas"], f"factura_{factura_id}.csv")

def gestion_reportes():
 

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

import plotly.express as px

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    # Verificar si hay datos en las facturas
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de facturas para analizar.")
        return

    # Crear una lista para desglosar productos en facturas
    productos_desglosados = []
    for _, fila in st.session_state["facturas"].iterrows():
        for producto in fila["Productos"]:
            productos_desglosados.append({
                "Producto": producto["Producto"],
                "Cantidad": producto["Cantidad"],
                "Subtotal": producto["Subtotal"],
                "Fecha": fila["Fecha"]
            })

    # Crear un DataFrame con los datos desglosados
    df_productos = pd.DataFrame(productos_desglosados)

    # Verificar si hay datos en el DataFrame desglosado
    if df_productos.empty:
        st.warning("No hay datos suficientes para generar análisis.")
        return

    # Análisis de ventas por producto
    st.subheader("Ventas por Producto")
    ventas_por_producto = df_productos.groupby("Producto").sum().reset_index()
    fig1 = px.bar(
        ventas_por_producto, 
        x="Producto", 
        y="Subtotal", 
        title="Ingresos por Producto", 
        labels={"Subtotal": "Ingresos ($)"},
        text="Subtotal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Análisis de cantidades vendidas por producto
    st.subheader("Cantidad Vendida por Producto")
    fig2 = px.pie(
        ventas_por_producto, 
        names="Producto", 
        values="Cantidad", 
        title="Distribución de Cantidades Vendidas"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Análisis temporal de ventas
    st.subheader("Ingresos Totales por Fecha")
    df_productos["Fecha"] = pd.to_datetime(df_productos["Fecha"])
    ingresos_por_fecha = df_productos.groupby("Fecha").sum().reset_index()
    fig3 = px.line(
        ingresos_por_fecha, 
        x="Fecha", 
        y="Subtotal", 
        title="Evolución de Ingresos en el Tiempo",
        labels={"Subtotal": "Ingresos ($)", "Fecha": "Fecha"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Gráficos interactivos generados correctamente.")

# Navegación entre módulos
if st.session_state["auth"]:
    if st.session_state["modulo_seleccionado"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo_seleccionado"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo_seleccionado"] == "Generar Factura":
        gestion_facturas()
    elif st.session_state["modulo_seleccionado"] == "Generar Reportes":
        gestion_reportes()
    elif st.session_state["modulo_seleccionado"] == "Análisis de Ventas":
        analisis_ventas()
else:
    st.warning("Por favor, inicia sesión para continuar.")
