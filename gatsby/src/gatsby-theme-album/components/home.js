import React from "react"
import { StaticImage } from "gatsby-plugin-image"

const Home = () => {
  return (
    <div>
        <StaticImage className="logo" src="https://raw.githubusercontent.com/HenriquesLab/DL4MicEverywhere/main/docs/images/policy.png" alt="DL4MicEverywhere offers an easy-to-use gateway to deep learning techniques for bioimage analysis." placeholder="blurred" fit="contain"/>
    </div>
  )
}

export default Home


