    class PuzzleSolver:
        def __init__(self, base64puzzle, base64piece):
            self.puzzle = base64puzzle
            self.piece = base64piece
            self.methods = [
                cv2.TM_CCOEFF_NORMED,
                cv2.TM_CCORR_NORMED
            ]
    
        def get_position(self):
            try:
                results = []
    
                puzzle = self.__background_preprocessing()
                piece = self.__piece_preprocessing()
    
                for method in self.methods:
                    matched = cv2.matchTemplate(puzzle, piece, method)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
                    if method == cv2.TM_SQDIFF_NORMED:
                        results.append((min_loc[0], 1 - min_val))
                    else:
                        results.append((max_loc[0], max_val))
    
                enhanced_puzzle = self.__enhanced_preprocessing(puzzle)
                enhanced_piece = self.__enhanced_preprocessing(piece)
    
                for method in self.methods:
                    matched = cv2.matchTemplate(enhanced_puzzle, enhanced_piece, method)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
                    if method == cv2.TM_SQDIFF_NORMED:
                        results.append((min_loc[0], 1 - min_val))
                    else:
                        results.append((max_loc[0], max_val))
    
                edge_puzzle = self.__edge_detection(puzzle)
                edge_piece = self.__edge_detection(piece)
    
                matched = cv2.matchTemplate(edge_puzzle, edge_piece, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
                results.append((max_loc[0], max_val))
    
                results.sort(key=lambda x: x[1], reverse=True)
                return results[0][0]
    
            except Exception as e:
                puzzle = self.__background_preprocessing()
                piece = self.__piece_preprocessing()
                matched = cv2.matchTemplate(puzzle, piece, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
                return max_loc[0]
    
        def __background_preprocessing(self):
            img = self.__img_to_array(self.piece)
            background = self.__sobel_operator(img)
            return background
    
        def __piece_preprocessing(self):
            img = self.__img_to_array(self.puzzle)
            template = self.__sobel_operator(img)
            return template
    
        def __enhanced_preprocessing(self, img):
            if len(img.shape) == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(img)
    
            return enhanced
    
        def __edge_detection(self, img):
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
    
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
            edges = cv2.Canny(blurred, 50, 150)
    
            return edges
    
        def __sobel_operator(self, img):
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
    
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
    
            grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3)
    
            abs_grad_x = cv2.convertScaleAbs(grad_x)
            abs_grad_y = cv2.convertScaleAbs(grad_y)
    
            grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    
            grad = cv2.normalize(grad, None, 0, 255, cv2.NORM_MINMAX)
    
            return grad
    
        def __img_to_array(self, base64_input):
            try:
                img_data = base64.b64decode(base64_input)
                img_array = np.frombuffer(img_data, dtype=np.uint8)
    
                decoded_img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
    
                if decoded_img is None:
                    raise ValueError("Failed to decode image")
    
                if len(decoded_img.shape) == 2:
                    decoded_img = cv2.cvtColor(decoded_img, cv2.COLOR_GRAY2BGR)
                elif decoded_img.shape[2] == 4:
                    decoded_img = cv2.cvtColor(decoded_img, cv2.COLOR_RGBA2BGR)
    
                return decoded_img
    
            except Exception as e:
                raise ValueError(f"Image processing error: {str(e)}")
    
    
    
    class CaptchaSolver:
        def __init__(self, iid: str, did: str, device_type: str, device_brand: str, country: str, proxy: str = None):
            self.iid = iid
            self.did = did
            self.device_type = device_type
            self.device_brand = device_brand
    
            self.host = 'rc-verification-sg.tiktokv.com'
          #  self.host = 'verification-va.tiktok.com'
            self.host_region = self.host.split('-')[2].split('.')[0]
          #  self.host_region = 'va'
            self.country = country
    
            # Using proxies in the requests session constructor directly
            if proxy:
                self.session = requests.Session()
                self.session.proxies = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }
            else:
                self.session = requests.Session()
    
        def get_captcha(self):
            params = f'lang=en&app_name=musical_ly&h5_sdk_version=2.33.7&h5_sdk_use_type=cdn&sdk_version=2.3.4.i18n&iid={self.iid}&did={self.did}&device_id={self.did}&ch=googleplay&aid=1233&os_type=0&mode=slide&tmp={int(time.time())}{random.randint(111, 999)}&platform=app&webdriver=undefined&verify_host=https%3A%2F%2F{self.host_region}%2F&locale=en&channel=googleplay&app_key&vc=32.9.5&app_version=32.9.5&session_id&region={self.host_region}&use_native_report=1&use_jsb_request=1&orientation=2&resolution=720*1280&os_version=25&device_brand={self.device_brand}&device_model={self.device_type}&os_name=Android&version_code=3275&device_type={self.device_type}&device_platform=Android&type=verify&detail=&server_sdk_env=&imagex_domain&subtype=slide&challenge_code=99996&triggered_region={self.host_region}&cookie_enabled=true&screen_width=360&screen_height=640&browser_language=en&browser_platform=Linux%20i686&browser_name=Mozilla&browser_version=5.0%20%28Linux%3B%20Android%207.1.2%3B%20{self.device_type}%20Build%2FN2G48C%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F86.0.4240.198%20Mobile%20Safari%2F537.36%20BytedanceWebview%2Fd8a21c6'
            sig = sign(params, '', "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233)
            headers = {
                'X-Tt-Request-Tag': 'n=1;t=0',
                'X-Vc-Bdturing-Sdk-Version': '2.3.4.i18n',
                'X-Tt-Bypass-Dp': '1',
                'Content-Type': 'application/json; charset=utf-8',
                'X-Tt-Dm-Status': 'login=0;ct=0;rt=7',
                'X-Tt-Store-Region': self.country,
                'X-Tt-Store-Region-Src': 'did',
                'User-Agent': f'com.zhiliaoapp.musically/2023209050 (Linux; U; Android 7.1.2; en_{self.country.upper()}; {self.device_type}; Build/N2G48C;tt-ok/3.12.13.4-tiktok)',
                "x-ss-req-ticket": sig["x-ss-req-ticket"],
                "x-ss-stub": sig["x-ss-stub"],
                "X-Gorgon": sig["x-gorgon"],
                "X-Khronos": str(sig["x-khronos"]),
                "X-Ladon": sig["x-ladon"],
                "X-Argus": sig["x-argus"]
            }
    
            response = self.session.get(
                f'https://{self.host}/captcha/get?{params}',
                headers=headers
            ).json()
    
            return response
    
        def verify_captcha(self, data):
            params = f'lang=en&app_name=musical_ly&h5_sdk_version=2.33.7&h5_sdk_use_type=cdn&sdk_version=2.3.4.i18n&iid={self.iid}&did={self.did}&device_id={self.did}&ch=googleplay&aid=1233&os_type=0&mode=slide&tmp={int(time.time())}{random.randint(111, 999)}&platform=app&webdriver=undefined&verify_host=https%3A%2F%2F{self.host}%2F&locale=en&channel=googleplay&app_key&vc=32.9.5&app_version=32.9.5&session_id&region={self.host_region}&use_native_report=1&use_jsb_request=1&orientation=2&resolution=720*1280&os_version=25&device_brand={self.device_brand}&device_model={self.device_type}&os_name=Android&version_code=3275&device_type={self.device_type}&device_platform=Android&type=verify&detail=&server_sdk_env=&imagex_domain&subtype=slide&challenge_code=99996&triggered_region={self.host_region}&cookie_enabled=true&screen_width=360&screen_height=640&browser_language=en&browser_platform=Linux%20i686&browser_name=Mozilla&browser_version=5.0%20%28Linux%3B%20Android%207.1.2%3B%20{self.device_type}%20Build%2FN2G48C%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F86.0.4240.198%20Mobile%20Safari%2F537.36%20BytedanceWebview%2Fd8a21c6'
            sig = sign(params, '', "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233)
            headers = {
                'X-Tt-Request-Tag': 'n=1;t=0',
                'X-Vc-Bdturing-Sdk-Version': '2.3.4.i18n',
                'X-Tt-Bypass-Dp': '1',
                'Content-Type': 'application/json; charset=utf-8',
                'X-Tt-Dm-Status': 'login=0;ct=0;rt=7',
                'X-Tt-Store-Region': self.country,
                'X-Tt-Store-Region-Src': 'did',
                'User-Agent': f'com.zhiliaoapp.musically/2023209050 (Linux; U; Android 7.1.2; en_{self.country.upper()}; {self.device_type}; Build/N2G48C;tt-ok/3.12.13.4-tiktok)',
                "x-ss-req-ticket": sig["x-ss-req-ticket"],
                "x-ss-stub": sig["x-ss-stub"],
                "X-Gorgon": sig["x-gorgon"],
                "X-Khronos": str(sig["x-khronos"]),
                "X-Ladon": sig["x-ladon"],
                "X-Argus": sig["x-argus"]
            }
    
            response = self.session.post(
                f'https://{self.host}/captcha/verify?{params}',
                headers=headers,
                json=data
            ).json()
    
            return response
    
        def start(self) -> None:
            try:
                _captcha = self.get_captcha()
    
                captcha_data = _captcha["data"]["challenges"][0]
    
                captcha_id = captcha_data["id"]
                verify_id = _captcha["data"]["verify_id"]
    
                puzzle_img = self.session.get(captcha_data["question"]["url1"]).content
                piece_img = self.session.get(captcha_data["question"]["url2"]).content
    
                puzzle_b64 = base64.b64encode(puzzle_img)
                piece_b64 = base64.b64encode(piece_img)
    
                solver = PuzzleSolver(puzzle_b64, piece_b64)
                max_loc = solver.get_position()
    
                rand_length = random.randint(50, 100)
                movements = []
    
                for i in range(rand_length):
                    progress = (i + 1) / rand_length
                    x_pos = round(max_loc * progress)
    
                    y_offset = random.randint(-2, 2) if i > 0 and i < rand_length - 1 else 0
                    y_pos = captcha_data["question"]["tip_y"] + y_offset
    
                    movements.append({
                        "relative_time": i * rand_length + random.randint(-5, 5),
                        "x": x_pos,
                        "y": y_pos
                    })
    
                verify_payload = {
                    "modified_img_width": 552,
                    "id": captcha_id,
                    "mode": "slide",
                    "reply": movements,
                    "verify_id": verify_id
                }
    
                return self.verify_captcha(verify_payload)
            except Exception as e:
                pass
    
    def send(device: str.split, proxy: str):
        return CaptchaSolver(device[0], device[1], device[2], device[3], device[4], proxy).start()
        
    def sign2(params, data: str or None = None, sec_device_id: str = '', aid: int = 1340, license_id: int = 1611921764, sdk_version_str: str = 'v04.04.05-ov-android', sdk_version: int = 134744640, platform: int = 0, unix: int = None):
        x_ss_stub = md5(data.encode()).hexdigest() if data != None else None
        if not unix: unix = int(time.time())
    
        return {
            'x-ladon'   : ladon.Ladon.encrypt(unix, license_id, aid),
            'x-argus'   : argus.Argus.get_sign(params, x_ss_stub, unix,
                platform        = platform,
                aid             = aid,
                license_id      = license_id,
                sec_device_id   = sec_device_id,
                sdk_version     = sdk_version_str, 
                sdk_version_int = sdk_version
            ),
        }
    
    class signature:
        def __init__(
            self, 
            params: str, 
            data: str, 
            cookies: str
        ) -> None:
    
            self.params = params
            self.data = data
            self.cookies = cookies
    
        def hash(self, data: str) -> str:
            return str(hashlib.md5(data.encode()).hexdigest())
    
        def calc_gorgon(self) -> str:
            gorgon = self.hash(self.params)
            if self.data:
                gorgon += self.hash(self.data)
            else:
                gorgon += str("0"*32)
            if self.cookies:
                gorgon += self.hash(self.cookies)
            else:
                gorgon += str("0"*32)
            gorgon += str("0"*32)
            return gorgon
    
        def get_value(self):
            return self.encrypt(self.calc_gorgon())
    
        def encrypt(self, data: str):
            unix = int(time.time())
            len = 0x14
            key = [
                0xDF,
                0x77,
                0xB9,
                0x40,
                0xB9,
                0x9B,
                0x84,
                0x83,
                0xD1,
                0xB9,
                0xCB,
                0xD1,
                0xF7,
                0xC2,
                0xB9,
                0x85,
                0xC3,
                0xD0,
                0xFB,
                0xC3,
            ]
    
            param_list = []
    
            for i in range(0, 12, 4):
                temp = data[8 * i : 8 * (i + 1)]
                for j in range(4):
                    H = int(temp[j * 2 : (j + 1) * 2], 16)
                    param_list.append(H)
    
            param_list.extend([0x0, 0x6, 0xB, 0x1C])
    
            H = int(hex(unix), 16)
    
            param_list.append((H & 0xFF000000) >> 24)
            param_list.append((H & 0x00FF0000) >> 16)
            param_list.append((H & 0x0000FF00) >> 8)
            param_list.append((H & 0x000000FF) >> 0)
    
            eor_result_list = []
    
            for A, B in zip(param_list, key):
                eor_result_list.append(A ^ B)
    
            for i in range(len):
    
                C = self.reverse(eor_result_list[i])
                D = eor_result_list[(i + 1) % len]
                E = C ^ D
    
                F = self.rbit(E)
                H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
                eor_result_list[i] = H
    
            result = ""
            for param in eor_result_list:
                result += self.hex_string(param)
    
            return {"X-Gorgon": ("0404b0d30000" + result), "X-Khronos": str(unix)}
    
        def rbit(self, num):
            result = ""
            tmp_string = bin(num)[2:]
    
            while len(tmp_string) < 8:
                tmp_string = "0" + tmp_string
    
            for i in range(0, 8):
                result = result + tmp_string[7 - i]
    
            return int(result, 2)
    
        def hex_string(self, num):
            tmp_string = hex(num)[2:]
    
            if len(tmp_string) < 2:
                tmp_string = "0" + tmp_string
    
            return tmp_string
    
        def reverse(self, num):
            tmp_string = self.hex_string(num)
    
            return int(tmp_string[1:] + tmp_string[:1], 16)