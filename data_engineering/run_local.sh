export AUDIENCE="https://kevin-tong-shopify-image-repo/" \
    CLIENT_ID="PtcUC3QMSGPg4CLMp06Lm0UpUz18ybQ3" \
    SCOPE="write:images read:images" \
    AWS_ROLE_ARN="arn:aws:iam::943493871826:role/shopify-openid-role" \
    AWS_ROLE_SESSION="shopify-session" \
    AWS_BUCKET="kevin-tong-shopify-image-repo"
python main.py