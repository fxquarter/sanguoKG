$(document).ready(function() {
            // 给搜索框添加聚焦效果
            $('#search-input').focus(function() {
                $(this).css('border-color', '#5b9bd5');
            }).blur(function() {
                $(this).css('border-color', '#ccc');
            });

            // 给筛选框添加聚焦效果
            $('#camp-select').focus(function() {
                $(this).css('border-color', '#5b9bd5');
            }).blur(function() {
                $(this).css('border-color', '#ccc');
            });
        });