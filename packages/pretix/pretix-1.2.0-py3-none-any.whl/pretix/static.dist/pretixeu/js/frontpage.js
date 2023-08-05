/*global $ */

function price_compare_calc() {
    var num = parseInt($("#price-comparison-number").val());
    var price = parseFloat($("#price-comparison-price").val());
    var payment = $('#price-comparison-payment').find(":selected").attr("value");
    var comp = $(".price-comparison-form").attr("data-competitor");
    var comp_price = 0,
        comp_price_payment = 0,
        pretix_price_payment = 0,
        pretix_price = (Math.min(0.025 * price, 15) * num);

    $("#price-competitor-payment").html("");
    if (comp === "xing") {
        comp_price = price > 0 ? (0.059 * price + 0.99) * num : 0;
        $("#price-competitor").text(comp_price.toFixed(2).replace(".", ",") + " €");
    } else if (comp == "eventbrite") {
        comp_price = price > 0 ? Math.min(9.95, 0.025 * price + 0.99) * num : 0;
        $("#price-competitor").text(comp_price.toFixed(2).replace(".", ",") + " €");
        if (payment === "stripe" || payment === "paypal" || payment == "debit") {
            comp_price_payment = num * (0.02 * price);
            $("#price-competitor-payment").html(
                "+ Zahlungsmittelgebühr (2 %) = " + comp_price_payment.toFixed(2).replace(".", ",") + " €"
                + "<br>Gesamt: <strong>" + (comp_price + comp_price_payment).toFixed(2).replace(".", ",") + " €</strong>"
            );
        }
    }
    
    $("#price-pretix").text(pretix_price.toFixed(2).replace(".", ",") + " €");
    if (payment === "stripe") {
        pretix_price_payment = num * (0.014 * price + 0.025);
        $("#price-pretix-payment").html(
            "+ Stripe (1,4 % + 0,25 €) = " + pretix_price_payment.toFixed(2).replace(".", ",") + " €"
            + "<br>Gesamt: <strong>" + (pretix_price + pretix_price_payment).toFixed(2).replace(".", ",") + " €</strong>"
        );
    } else if (payment === "paypal") {
        pretix_price_payment = num * (0.019 * price + 0.035);
        $("#price-pretix-payment").html(
            "+ PayPal (1,9 % + 0,35 €) = " + pretix_price_payment.toFixed(2).replace(".", ",") + " €"
            + "<br>Gesamt: <strong>" + (pretix_price + pretix_price_payment).toFixed(2).replace(".", ",") + " €</strong>"
        );
    } else {
        pretix_price_payment = 0;
        $("#price-pretix-payment").html(
            "&nbsp;<br>&nbsp;"
        );
    }
    var saving = comp_price + comp_price_payment - pretix_price - pretix_price_payment;
    $(".price-winner").toggleClass("better", saving > 0).toggleClass("worse", saving <= 0);
    $("#price-text").text("");
    if (num > 5000) {
        $("#price-text").html("<br>Für Events dieser Größenordnung sprechen Sie uns bitte auf rabattierte Preise an!");
    } else if (saving <= 0) {
        if (num * price > 100000) {
            $("#price-text").text("Das ist aber ein großes Event, sprechen Sie uns doch bitte auf ein konkurrenzfähiges Angebot an!");
        } else {
            $("#price-text").text("Den Preis können wir leider nicht schlagen – aber den Service!");
        }
    }
    $("#price-saved").text(saving.toFixed(2).replace(".", ",") + " €");

}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
    
    // Nav
    $(".nav-toggle").removeClass("sr-only");
    $("header.subpage nav, header.campain nav").addClass("hidden-xs");
    $(".nav-toggle").click(function () {
        if ($("header nav").hasClass("hidden-xs")) {
            $("header nav").hide().removeClass("hidden-xs");
        }
        $("header nav").slideToggle();
    });

    // Campain
    $("a.scroll").click(function (e) {
        $('html, body').animate({
            scrollTop: $($(this).attr("href")).offset().top
        }, 500);
        e.preventDefault();
        return;
    });

        // Typewriter
    $(".purpose").text("");
    $(".purpose").typed(
        {
            stringsElement: $('#typed-strings'),
            typeSpeed: 70,
            backDelay: 1000,
            loop: true
        }
    );

    if ($(".price-comparison-form").length) {
        price_compare_calc();
        $(".price-comparison-form .form-control").on("keydown keyup keypress change", price_compare_calc);
    }

    // Cookie
    $("#cookie_close").click(function (e) {
        document.cookie = "_eu_cookie_accepted=yes; expires=Tue, 01 Jan 2037 12:00:00 UTC; path=/";
        $("#cookie").slideUp();
        e.preventDefault();
        return true;
    });
    if (document.cookie.search("_eu_cookie_accepted") >= 0) {
        $("#cookie").remove();
    }
});

var _paq = _paq || [];
_paq.push(["disableCookies"]);
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function () {
    var u = "https://piwik.glokta.rami.io/";
    _paq.push(['setTrackerUrl', u + 'piwik.php']);
    _paq.push(['setSiteId', '6']);
    var d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0];
    g.type = 'text/javascript';
    g.async = true;
    g.defer = true;
    g.src = u + 'piwik.js';
    s.parentNode.insertBefore(g, s);
})();
