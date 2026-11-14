/* SmartEdu - Theme Scripts */
document.addEventListener('DOMContentLoaded', function () {
    // Number counters
    if (window.$) {
        $('.counter-number').each(function () {
            var $this = $(this);
            var countTo = parseInt($this.text(), 10);
            if (!isNaN(countTo) && countTo > 0) {
                $this.prop('Counter', 0).animate({
                    Counter: countTo
                }, {
                    duration: 2000,
                    easing: 'swing',
                    step: function (now) {
                        $this.text(Math.ceil(now));
                    }
                });
            }
        });

        $('#hamburger').on('click', function () {
            $('#hamburger').toggleClass('show');
            $('#overlay').toggleClass('show');
            $('.nav1').toggleClass('show');
        });
    }

    var imgs = document.querySelectorAll('.change-img');
    var imgsrc = document.querySelector('.set-img');
    if (imgs && imgs.length && imgsrc) {
        imgs.forEach(function (img) {
            img.addEventListener('click', function () {
                var innerImg = img.querySelector('img');
                if (!innerImg) return;
                var imgname = innerImg.getAttribute('name');
                imgs.forEach(function (el) { el.classList.remove('img-overlay'); });
                img.classList.add('img-overlay');
                document.querySelectorAll('.atd').forEach(function (el) { el.classList.add('d-none'); });
                var targetAtd = document.querySelector('.atd[name="' + imgname + '"]');
                if (targetAtd) targetAtd.classList.remove('d-none');
                imgsrc.setAttribute('src', innerImg.getAttribute('src'));
            });
        });
    }
});
