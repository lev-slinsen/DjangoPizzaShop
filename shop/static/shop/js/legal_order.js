$(document).ready(function(){
    $('#phone').mask('(00)000-00-00');
});

function validationAll() {
    if (
        document.getElementById("unp").classList.contains('is-valid')
        && document.getElementById("phone").classList.contains('is-valid')
        && document.getElementById("name_firm").classList.contains('is-valid')
        && document.getElementById("first_name").classList.contains('is-valid')
        && document.getElementById("delivery_date").classList.contains('is-valid')
        && document.getElementById("delivery_time").classList.contains('is-valid')
        && document.getElementById("delivery_address").classList.contains('is-valid')
        && document.getElementById("legal_address").classList.contains('is-valid')
        && document.getElementById("email").classList.contains('is-valid')
        && document.getElementById("payment").classList.contains('is-valid')
    ) {
        document.getElementById("order-submit").disabled = false;
        document.getElementById("alert-message").style.display = 'none';
    } else {
        document.getElementById("order-submit").disabled = true;
        document.getElementById("alert-message").style.display = 'block';
    }
}
validationAll();

function onPhoneInput(e) {
    var numb = e.target.value.match(/\d/g);
    var idx = numb.slice(0, 3).join("").indexOf('375')
    if (idx >= 0) {
        var toChange = numb.slice(3, numb.length).join('')
        e.target.value = toChange
    }
}
var phoneInput = document.getElementById("phone");
phoneInput.addEventListener('input', onPhoneInput);

function validateField(field, fieldId, count) {
    if (field.length < count) {
        document.getElementById(fieldId).className = 'form-control is-invalid';
        validationAll();
    } else {
        document.getElementById(fieldId).className = 'form-control is-valid';
        validationAll();
    }
}

function validateEmail() {
    let emailMasked = document.getElementById("email").value;
    validateField(emailMasked, "email", 5);
}

function validateUnp() {
    let unpMasked = document.getElementById("unp").value;
    validateField(unpMasked, "unp", 3);
}

function validatePhone() {
    let phoneMasked = document.getElementById("phone").value;
    var numb = phoneMasked.match(/\d/g);
    numb = numb.join("");
    validateField(numb, "phone", 9);
}

function validateDate() {
    let dateField = document.getElementById("delivery_date").value;
        validateField(dateField, "delivery_date", 3);
}

function validateTime() {
    validTime = document.querySelector('#delivery_time').value;
    validateField(validTime, "delivery_time", 1);
}
function validatePaymentWay() {
    validPayment = document.querySelector('#payment').value;
    validateField(validPayment, "payment", 1);
}

function validateAddress() {
    let address = document.getElementById("legal_address").value;
    validateField(address, "legal_address", 5);
}

function validateDeliveryAddress() {
    let address = document.getElementById("delivery_address").value;
    validateField(address, "delivery_address", 5);
}

function validateName() {
    let nameField = document.getElementById("first_name").value;
    validateField(nameField, "first_name", 3);
}

function validateNameFirm() {
    let NameFirmField = document.getElementById("name_firm").value;
    validateField(NameFirmField, "name_firm", 3);
}

function phoneNumberToDigits() {
    let phoneMasked = document.getElementById("phone").value;
    var numb = phoneMasked.match(/\d/g);
    numb = numb.join("");
    document.getElementById('phone').value = numb;
}

let submitBtn = document.getElementById('order-submit');
submitBtn.addEventListener('click', function(event){
    document.getElementById("order-submit").disabled = true;
    event.preventDefault();
    let order = localStorage.getItem('order');
    let dateField = document.getElementById("delivery_date");
    var newDate = moment(dateField.value).format("YYYY-MM-DD");
    dateField.value = newDate;
    phoneNumberToDigits();
    let redirectLink = '';
    let form = new FormData(document.querySelector("#order-form"));
    form.append("order", order);
    postData("/legal_order/", form);
});

function postData(url = '', data = {}) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    console.log(csrftoken);
    return fetch(url, {
        method: 'POST',
        redirect: 'manual',
        headers: {
          'X-CSRFToken': csrftoken
        },
        body: data,
    })
        .then(function(response) {
           return response.text();
           document.getElementById("order-submit").disabled = false;
        })
        .then(function(data) {
            let validPayment = document.querySelector('#payment').value;
            if (data === "error") {
                $('#ModalCenteredWarning').modal('show');
                return error = true;
            } else {
                if (validPayment === '2'){
                    localStorage.clear();
                    return window.location.href=data;
                } else {
                    $('#ModalCenteredSucces').modal('show');
                    localStorage.clear();
                }
            }

        })
}
$('#ModalCenteredSucces').on('hidden.bs.modal', function (e) {
    window.location="/"
});
$('#ModalCenteredWarning').on('hidden.bs.modal', function (e) {
    window.location="/"
});

//! moment.js locale configuration

(function (global, factory) {
   typeof exports === 'object' && typeof module !== 'undefined'
       && typeof require === 'function' ? factory(require('../moment')) :
   typeof define === 'function' && define.amd ? define(['../moment'], factory) :
   factory(global.moment)
}(this, (function (moment) { 'use strict';


    function plural(word, num) {
        var forms = word.split('_');
        return num % 10 === 1 && num % 100 !== 11 ? forms[0] : (num % 10 >= 2 && num % 10 <= 4 && (num % 100 < 10 || num % 100 >= 20) ? forms[1] : forms[2]);
    }
    function relativeTimeWithPlural(number, withoutSuffix, key) {
        var format = {
            'ss': withoutSuffix ? 'секунда_секунды_секунд' : 'секунду_секунды_секунд',
            'mm': withoutSuffix ? 'минута_минуты_минут' : 'минуту_минуты_минут',
            'hh': 'час_часа_часов',
            'dd': 'день_дня_дней',
            'MM': 'месяц_месяца_месяцев',
            'yy': 'год_года_лет'
        };
        if (key === 'm') {
            return withoutSuffix ? 'минута' : 'минуту';
        }
        else {
            return number + ' ' + plural(format[key], +number);
        }
    }
    var monthsParse = [/^янв/i, /^фев/i, /^мар/i, /^апр/i, /^ма[йя]/i, /^июн/i, /^июл/i, /^авг/i, /^сен/i, /^окт/i, /^ноя/i, /^дек/i];

    // http://new.gramota.ru/spravka/rules/139-prop : § 103
    // Сокращения месяцев: http://new.gramota.ru/spravka/buro/search-answer?s=242637
    // CLDR data:          http://www.unicode.org/cldr/charts/28/summary/ru.html#1753
    var ru = moment.defineLocale('ru', {
        months : {
            format: 'января_февраля_марта_апреля_мая_июня_июля_августа_сентября_октября_ноября_декабря'.split('_'),
            standalone: 'январь_февраль_март_апрель_май_июнь_июль_август_сентябрь_октябрь_ноябрь_декабрь'.split('_')
        },
        monthsShort : {
            // по CLDR именно "июл." и "июн.", но какой смысл менять букву на точку ?
            format: 'янв._февр._мар._апр._мая_июня_июля_авг._сент._окт._нояб._дек.'.split('_'),
            standalone: 'янв._февр._март_апр._май_июнь_июль_авг._сент._окт._нояб._дек.'.split('_')
        },
        weekdays : {
            standalone: 'воскресенье_понедельник_вторник_среда_четверг_пятница_суббота'.split('_'),
            format: 'воскресенье_понедельник_вторник_среду_четверг_пятницу_субботу'.split('_'),
            isFormat: /\[ ?[Вв] ?(?:прошлую|следующую|эту)? ?\] ?dddd/
        },
        weekdaysShort : 'вс_пн_вт_ср_чт_пт_сб'.split('_'),
        weekdaysMin : 'вс_пн_вт_ср_чт_пт_сб'.split('_'),
        monthsParse : monthsParse,
        longMonthsParse : monthsParse,
        shortMonthsParse : monthsParse,

        // полные названия с падежами, по три буквы, для некоторых, по 4 буквы, сокращения с точкой и без точки
        monthsRegex: /^(январ[ья]|янв\.?|феврал[ья]|февр?\.?|марта?|мар\.?|апрел[ья]|апр\.?|ма[йя]|июн[ья]|июн\.?|июл[ья]|июл\.?|августа?|авг\.?|сентябр[ья]|сент?\.?|октябр[ья]|окт\.?|ноябр[ья]|нояб?\.?|декабр[ья]|дек\.?)/i,

        // копия предыдущего
        monthsShortRegex: /^(январ[ья]|янв\.?|феврал[ья]|февр?\.?|марта?|мар\.?|апрел[ья]|апр\.?|ма[йя]|июн[ья]|июн\.?|июл[ья]|июл\.?|августа?|авг\.?|сентябр[ья]|сент?\.?|октябр[ья]|окт\.?|ноябр[ья]|нояб?\.?|декабр[ья]|дек\.?)/i,

        // полные названия с падежами
        monthsStrictRegex: /^(январ[яь]|феврал[яь]|марта?|апрел[яь]|ма[яй]|июн[яь]|июл[яь]|августа?|сентябр[яь]|октябр[яь]|ноябр[яь]|декабр[яь])/i,

        // Выражение, которое соотвествует только сокращённым формам
        monthsShortStrictRegex: /^(янв\.|февр?\.|мар[т.]|апр\.|ма[яй]|июн[ья.]|июл[ья.]|авг\.|сент?\.|окт\.|нояб?\.|дек\.)/i,
        longDateFormat : {
            LT : 'H:mm',
            LTS : 'H:mm:ss',
            L : 'DD.MM.YYYY',
            LL : 'D MMMM YYYY г.',
            LLL : 'D MMMM YYYY г., H:mm',
            LLLL : 'dddd, D MMMM YYYY г., H:mm'
        },
        calendar : {
            sameDay: '[Сегодня, в] LT',
            nextDay: '[Завтра, в] LT',
            lastDay: '[Вчера, в] LT',
            nextWeek: function (now) {
                if (now.week() !== this.week()) {
                    switch (this.day()) {
                        case 0:
                            return '[В следующее] dddd, [в] LT';
                        case 1:
                        case 2:
                        case 4:
                            return '[В следующий] dddd, [в] LT';
                        case 3:
                        case 5:
                        case 6:
                            return '[В следующую] dddd, [в] LT';
                    }
                } else {
                    if (this.day() === 2) {
                        return '[Во] dddd, [в] LT';
                    } else {
                        return '[В] dddd, [в] LT';
                    }
                }
            },
            lastWeek: function (now) {
                if (now.week() !== this.week()) {
                    switch (this.day()) {
                        case 0:
                            return '[В прошлое] dddd, [в] LT';
                        case 1:
                        case 2:
                        case 4:
                            return '[В прошлый] dddd, [в] LT';
                        case 3:
                        case 5:
                        case 6:
                            return '[В прошлую] dddd, [в] LT';
                    }
                } else {
                    if (this.day() === 2) {
                        return '[Во] dddd, [в] LT';
                    } else {
                        return '[В] dddd, [в] LT';
                    }
                }
            },
            sameElse: 'L'
        },
        relativeTime : {
            future : 'через %s',
            past : '%s назад',
            s : 'несколько секунд',
            ss : relativeTimeWithPlural,
            m : relativeTimeWithPlural,
            mm : relativeTimeWithPlural,
            h : 'час',
            hh : relativeTimeWithPlural,
            d : 'день',
            dd : relativeTimeWithPlural,
            M : 'месяц',
            MM : relativeTimeWithPlural,
            y : 'год',
            yy : relativeTimeWithPlural
        },
        meridiemParse: /ночи|утра|дня|вечера/i,
        isPM : function (input) {
            return /^(дня|вечера)$/.test(input);
        },
        meridiem : function (hour, minute, isLower) {
            if (hour < 4) {
                return 'ночи';
            } else if (hour < 12) {
                return 'утра';
            } else if (hour < 17) {
                return 'дня';
            } else {
                return 'вечера';
            }
        },
        dayOfMonthOrdinalParse: /\d{1,2}-(й|го|я)/,
        ordinal: function (number, period) {
            switch (period) {
                case 'M':
                case 'd':
                case 'DDD':
                    return number + '-й';
                case 'D':
                    return number + '-го';
                case 'w':
                case 'W':
                    return number + '-я';
                default:
                    return number;
            }
        },
        week : {
            dow : 1, // Monday is the first day of the week.
            doy : 4  // The week that contains Jan 4th is the first week of the year.
        }
    });

    return ru;

})));



