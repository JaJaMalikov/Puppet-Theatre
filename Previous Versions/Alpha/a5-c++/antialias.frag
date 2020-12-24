uniform sampler2D texture;
uniform vec2 imgSize;

void main()
{
	vec2 coords = gl_TexCoord[0].xy;
	vec2 uv = ( coords - 0.5 ) * ( imgSize + 2.0 ) / imgSize + vec2( 0.5, 0.5 );
	float aa_edge = length( max( abs( coords * imgSize - imgSize / 2.0 ) - ( imgSize / 2.0 - vec2( 1.5, 1.5 )), 0.0 ));
	vec4 pixel = texture2D( texture, uv );
	gl_FragColor = gl_Color * pixel;
	gl_FragColor.w = gl_Color.w * ( 1.0 - aa_edge );
}
