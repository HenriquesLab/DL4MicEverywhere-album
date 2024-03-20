module.exports = {
  pathPrefix: `/DL4MicEverywhere-album`,
  siteMetadata: {
    title: 'DL4MicEverywhere Album solutions',
    subtitle: 'Cutting-edge deep learning techniques for bioimage analysis',
    catalog_url: 'https://github.com/HenriquesLab/DL4MicEverywhere-album',
    menuLinks:[
      {
         name:'Catalog',
         link:'/catalog'
      },
      {
         name:'About',
         link:'/about'
      },
    ]
  },
  plugins: [{ resolve: `gatsby-theme-album`, options: {} }],
}
