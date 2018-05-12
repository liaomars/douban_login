import requests
from PIL import Image
from pyquery import PyQuery as pq

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
    'Referer': 'https://accounts.douban.com/login',
    'Host': 'accounts.douban.com',
    'Origin': 'https://accounts.douban.com',
}


class DoubanLogin(object):
    def __init__(self, email, password):
        # 登录地址
        self.login_url = 'https://www.douban.com/accounts/login'
        # session对象
        self._session = requests.session()
        # form data
        self.form_data = {
            'redir': 'https://www.douban.com',
            'form_email': email,
            'form_password': password,
            'login': '登录'
        }

    def login(self):
        # 访问登录url
        res = self._session.get(self.login_url, headers=HEADER)
        # 判断是否需要验证码
        jq = pq(res.text)
        captcha_url = jq('#captcha_image').attr('src')

        # 如果有验证码，form_data要增增加 captcha-solution,captcha-id
        if captcha_url:
            captcha_id = self.get_captcha(jq)
            if captcha_id:
                # 显示验证码图片
                self.get_captcha_img(captcha_id)

                img = Image.open('.captcha.png')
                img.show()
                captcha = input('请输入图片验证码')
                self.form_data.update({'captcha-solution': captcha, 'captcha-id': captcha_id})
            else:
                print('没有获取到captcha_id参数')

        # 发起登录请求
        html = self._session.post('https://accounts.douban.com/login', data=self.form_data, headers=HEADER)
        print(html.text)

    def get_captcha(self, jq):
        """
        获取captcha_id 提交和获取验证码图片要用到
        :param jq:
        :return:
        """
        captcha_id = jq('input[name="captcha-id"]').val()
        return captcha_id

    def get_captcha_img(self, captcha_id):
        """
        获取验证码图片
        :param captcha_id:
        :return:
        """
        url = 'https://www.douban.com/misc/captcha?id={}&size=s'
        res = self._session.get(url.format(captcha_id), headers=HEADER)
        with open('.captcha.png', 'wb') as f:
            f.write(res.content)


if __name__ == '__main__':
    email = input('请输入注册时的邮箱/用户名/手机:')
    password = input('请输入密码:')
    douban = DoubanLogin(email, password)
    douban.login()
