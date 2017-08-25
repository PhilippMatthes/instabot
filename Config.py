class Config:

    topics = ["graphic","render","cartoon","daily","art","design","cinema4d","animation","cg","illustration"]
    delay = 35
    start_url = "https://www.instagram.com/accounts/login/"


    # The following (xpath) classes need to be refreshed every now and then.
    # they define, where elements are located on Instagram. Sometimes,
    # classes are Changed (eg. "coreSpriteHeartOpen" to "coreSpriteLikeHeartOpen")
    # this results in vast amount of errors and needs to be corrected.
    first_ele_xpath = "//*[contains(@class, '_si7dy')]"
    sections_xpath = "//*[contains(@class, '_6jvgy')]"
    local_name_xpath = ".//a[@class='_4zhc5 notranslate _j7lfh']"
    local_button_xpath = ".//*[@class='_ah57t _6y2ah _i46jh _rmr7s']"
    following_xpath = "//*[contains(@class, '_s53mj')]"
    follow_xpath = "//*[contains(@class, '_qv64e _gexxb _4tgw8 _njrw0')]"
    unfollow_xpath = "//*[contains(@class, '_qv64e _t78yp _r9b8f _njrw0')]"
    comment_xpath = "//*[contains(@class, '_bilrf')]"
    error_xpath = "//*[contains(@class, 'error-container -cx-PRIVATE-ErrorPage__errorContainer')]"

    author_xpath = "//*[contains(@class, '_2g7d5 notranslate _iadoq')]"
    next_button_xpath = "//*[contains(@class, '_3a693 coreSpriteRightPaginationArrow')]"
    like_button_xpath = "//*[contains(@class, '_8scx2 coreSpriteHeartOpen')]"
    like_button_full_xpath = "//*[contains(@class, '_8scx2 coreSpriteHeartFull')]"

    # Available comments: the first {} is replaced with the username
    # the second is replaced with a smiley. Note that UTF-8 smileys are only
    # supported by Firefox driver which may corrupt some timed functionalities.
    comments = [ "Nice @{} {}","@{} cool {} ","Great style @{} {}","Amazing @{} {}",\
                "Awesome @{} {}","Fantastic @{} {}","@{} {}","Brilliant one @{} {}",\
                "Pretty nice @{} {}","Awesome feed @{} {}","I like your feed @{} {}",\
                "Top @{} {}", "Really cool works @{}! {}", "@{} Rad!!! {}",\
                "This is cool @{} {}", "Love this @{} {}", "Great @{}! {}", "Yeah @{} {}"]
    smileys = [  ":)",":D","=D","=)",";)",":)",":)",";D" ]
