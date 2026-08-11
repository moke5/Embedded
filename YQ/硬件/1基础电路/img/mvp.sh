src="."
dst="../../STM32/img/"

# 填写你确定的文件名
arr=(
"rBJlJmJaPK-AEtJ2AACWxQMTzkk620.png"
"rBJlJmJaPK-AQrHkAAMo1-NCi3s820.png"
"rBJlJmJaPK-AHuDBAAC6jDe3Xb4953.png"
"rBJlJmJaPK-AHMHCAADbceh1CSU925.png"
"rBJlJmJaPK-APfQZAADieUaROUY142.png"
"rBJlJmJaPK-AJlH2AABMlILkDog272.png"
"rBJlJmJaPK-AaN0cAAFUPoI7c_4753.png"
"rBJlJmJaPK-AZ6qPAAGAcvfi_hM073.png"
"rBJlJmJaf4KADFAaAAJOEx_Jf24296.png"
"rBJlJmJaf4KAB3UFAAHZkLWNqGY108.png"
"rBJlJmJaf4KAJRlyAAAXhWyRyhM929.png"
"rBJlJmJaf4KAHcrkAAAdCWNYwkw681.png"
"rBJlJmJaf4KAf7nfAADJuwllKEI035.png"
"rBJlJmJaf4KAD5syAACI5J6BawE442.png"
"rBJlJmJdS3mAUANjAALMNbIH_Jg270.png"
"rBJlJmJdS3mAX2BCAAB4doKMB6o190.png"
"rBJlJmJdS3mANQznAAAuNNQR1h4830.png"
"rBJlJmJdS3mAYvf3AABL1GA4ajY008.png"
"rBJlJmJdS3mAI6msAAA-H-q8i4A976.png"
)

for name in "${arr[@]}"; do
    mv "${src}/${name}" "${dst}"
done
