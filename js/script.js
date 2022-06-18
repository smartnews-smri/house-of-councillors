let data = {};
const DESCRIPTIONS = {
  kaiha: "各会派（政党）の名称や任期別の議員数。なお欠員があるため合計の議員数と定数は必ず一致するわけではありません",
  giin: "各議員の名前、選挙区、当選回数、経歴など。省略された経歴などを閲覧する場合はファイルをダウンロードしてください",
  gian: "第153回国会以降に提出された議案（法律案、決議案、予算案など）。第208回国会までで約8,600件。データ量が多いため最新500件のみ表示しています",
  syuisyo: "第1回国会以降に提出された質問主意書。第208回国会までで約6,800件。データ量が多いため最新500件のみ表示しています"
};

const init = () => {

  const addCommas = (num) => {
    return String(num).replace( /(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
  }

  const showContent = () => {
    const tab = $("#tabs").find(".tab.selected").attr("for");

    const updateTable = (tab) => {
      $tbody = $("#data-table").find("tbody").empty();
      $thead = $("#data-table").find("thead").empty();

      // Header
      let tr = '<tr>';
      data[tab][0].map(cell => {
        tr += '<th>' + cell + '</th>';
      });
      tr += '</tr>';
      $thead.append(tr);

      // Content
      data[tab].slice(1).map(row => {
        let tr = '<tr>';

        row.map(cell => {
          if (cell.toString().slice(0, 8) === "https://") {
            tr += '<td><a href="' + cell + '" target="_blank">' + cell + '</a></td>';
          } else {
            tr += '<td>' + cell + '</td>';
          }
        });

        tr += '</tr>';

        $tbody.append(tr);
      });
    }

    const updateDownloadLink = (tab) => {
      $("#download-full-csv").attr("href", "./data/" + tab + ".csv");
      $("#download-full-csv").attr("download", tab + ".csv");
      $("#download-full-json").attr("href", "./data/" + tab + ".json");
      $("#download-full-json").attr("download", tab + ".json");
    }

    $("#tab-info-description").text(DESCRIPTIONS[tab]);
    $("#input-table-search").val("");
    $("#download-current-wrapper").removeClass("available");

    updateTable(tab);
    updateDownloadLink(tab);
  }

  const loadData = () => {

    const showData = () => {

      showContent();
      $("#cover").fadeOut();
    }

    const updateData = (updatetime) => {

      let count = 0;

      const targets = [
        "kaiha",
        "giin",
        "gian",
        "syuisyo"
      ];

      targets.map((target) => {
        let file = "data/" + target + ".json";
        if (target === "gian" || target === "syuisyo") file = file.replace(".json", "_sample.json");
        $.getJSON(file, function(json){
          data[target] = json;
          count++;

          if (count >= targets.length) {
            showData();
          }
        });
      });
    }

    updateData();
  }

  const bindEvents = () => {

    $("#tabs").find(".tab").on("click", function(){
      if (!$(this).hasClass("selected")) {
        $(this).siblings(".tab").removeClass("selected");
        $(this).addClass("selected");
        showContent();
      }
    });

    $("#download-current").on("click", function(e){
      e.preventDefault();

      if (!$(this).closest("#download-current-wrapper").hasClass("available")) {
        return false;
      }

      const getTable = () => {
        let result = "";
        $("#data-table").find("tr").each(function(){
          if ($(this).is(':visible')) {
            $(this).find("td,th").each(function(){
              result += "," + $(this).text();
            });
            result += "\n";
          }
        });

        result = result.slice(1);
        result = result.slice(0, -1);
        result = result.replaceAll("\n,", "\n");

        return result;
      }

      const data = getTable();
      const filename = ".csv";
      const bom = new Uint8Array([0xef, 0xbb, 0xbf]);
      const blob = new Blob([bom, data], {type: "text/csv"});

      if (window.navigator.msSaveBlob) {
        window.navigator.msSaveBlob(blob, filename);
      } else {
        const url = (window.URL || window.webkitURL).createObjectURL(blob);
        const d = document.createElement("a");
        d.href = url;
        d.download = filename;
        d.click();
        (window.URL || window.webkitURL).revokeObjectURL(url);
      }
    });

    $("#social-button-copy").on("click", function(e){
      e.preventDefault();
      let text = "参議院オープンデータ - スマートニュース メディア研究所\nhttps://smartnews-smri.github.io/house-of-councillors/";
      let $textarea = $('<textarea></textarea>');
      $textarea.text(text);
      $(this).append($textarea);
      $textarea.select();
      document.execCommand('copy');
      $textarea.remove();
      let $copyText = $(this).next(".text-copy");
      $copyText.addClass("copied");

      setTimeout(function() {
        $copyText.removeClass("copied");
      }, 3000);
    });

    $("#input-table-search").on("change", function(e){
      let val = $(this).val();

      if (val == "") {
        $("#download-current-wrapper").removeClass("available");
      } else {
        $("#download-current-wrapper").addClass("available");
      }

      $("#data-table").find("tbody").find("tr").each(function(){
        let hit = false;
        $(this).find("td").each(function(){
          let cell = $(this).text();
          if (cell.indexOf(val) !== -1) hit = true;
        });

        if (hit) {
          $(this).show();
        } else {
          $(this).hide();
        }
      });

    });
  }

  loadData();
  bindEvents();
}


$(function(){
  init();
});
