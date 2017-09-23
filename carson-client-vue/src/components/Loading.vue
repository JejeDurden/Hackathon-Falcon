<template>
	<div id="circleG">
		<div id="circleG_1" class="circleG"></div>
		<div id="circleG_2" class="circleG"></div>
		<div id="circleG_3" class="circleG"></div>
	</div>
</template>
<script>
export default {
  name: 'loading'
}
</script>

<style scoped lang="SASS">
#circleG{
	margin:auto;
}

.circleG{
	background-color:rgb(255,255,255);
	float:left;
	height: 10px;
    margin-left: 5px;
    width: 10px;
	animation-name:bounce_circleG;
		-o-animation-name:bounce_circleG;
		-ms-animation-name:bounce_circleG;
		-webkit-animation-name:bounce_circleG;
		-moz-animation-name:bounce_circleG;
	animation-duration:1.1675s;
		-o-animation-duration:1.1675s;
		-ms-animation-duration:1.1675s;
		-webkit-animation-duration:1.1675s;
		-moz-animation-duration:1.1675s;
	animation-iteration-count:infinite;
		-o-animation-iteration-count:infinite;
		-ms-animation-iteration-count:infinite;
		-webkit-animation-iteration-count:infinite;
		-moz-animation-iteration-count:infinite;
	animation-direction:normal;
		-o-animation-direction:normal;
		-ms-animation-direction:normal;
		-webkit-animation-direction:normal;
		-moz-animation-direction:normal;
	border-radius:20px;
		-o-border-radius:20px;
		-ms-border-radius:20px;
		-webkit-border-radius:20px;
		-moz-border-radius:20px;
}

#circleG_1{
	animation-delay:0.2295s;
		-o-animation-delay:0.2295s;
		-ms-animation-delay:0.2295s;
		-webkit-animation-delay:0.2295s;
		-moz-animation-delay:0.2295s;
}

#circleG_2{
	animation-delay:0.5455s;
		-o-animation-delay:0.5455s;
		-ms-animation-delay:0.5455s;
		-webkit-animation-delay:0.5455s;
		-moz-animation-delay:0.5455s;
}

#circleG_3{
	animation-delay:0.6985s;
		-o-animation-delay:0.6985s;
		-ms-animation-delay:0.6985s;
		-webkit-animation-delay:0.6985s;
		-moz-animation-delay:0.6985s;
}



@keyframes bounce_circleG{
	0%{}

	50%{
		background-color:rgb(0,0,0);
	}

	100%{}
}

@-o-keyframes bounce_circleG{
	0%{}

	50%{
		background-color:rgb(0,0,0);
	}

	100%{}
}

@-ms-keyframes bounce_circleG{
	0%{}

	50%{
		background-color:rgb(0,0,0);
	}

	100%{}
}

@-webkit-keyframes bounce_circleG{
	0%{}

	50%{
		background-color:rgb(0,0,0);
	}

	100%{}
}

@-moz-keyframes bounce_circleG{
	0%{}

	50%{
		background-color:rgb(0,0,0);
	}

	100%{}
}
</style>
