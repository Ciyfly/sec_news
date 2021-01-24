//所有jquery插件其实都是在jquery的原型上添加的方法

jQuery.fn.waterfall = function() {
	console.log("插件被调用了");

	//this指向的是被调用的DOM
	console.log(this);

	//在items中实现item的瀑布流布局

	//获取所有需要定位的子元素
	var items = $(this).children();

	//为items设置相对定位
	$(this).css({
		position: 'relative'
	})

	//计算每列的宽度（可以根据要显示的列数来计算）

	var column = 5;
	var cWidth = $(this).width();
	console.log(cWidth);
	var width = cWidth / column;
	console.log(width);

	//定义一个数组，来记录每一行的五个子元素的高度
	var h = [];

	//设置子元素的间距
	var gap = 10;

	//给每一列的子元素设置宽度
	items.width(width - 10);

	//需要为不同的子元素设置不同的定位坐标
	items.each(function(key,val) {

		//如果是第一行，top值都为0，left值为索引值乘以宽度
		console.log(this);


		//根据列数来判断是否为第一行的元素
		if(key < column){
			h.push($(this).height());
			$(this).css({
				position: 'absolute',
				left: key * width,
				top: 0
			})
		}else{
			var min_val = h[0];
			var min_key = 0;

			for(var i = 0;i < h.length;i++) {
				if(h[i] < min_val) {
					min_val = h[i];
					min_key = i;
				}
			}

			//更新最小列的宽度
			h[min_key] += $(this).height(); 

			$(this).css({
				position: 'absolute',
				left: min_key * width,
				top: min_val 
			})


		}
	});


	//计算整个瀑布流页面的最高高度,要不后面的html代码会被隐藏
	h.sort(function(a,b){
		return a < b;
	});

	$(this).height(h[0]);
}