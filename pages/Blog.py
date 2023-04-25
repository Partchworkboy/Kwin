import streamlit as st
import pandas as pd

# Set form title and configuration for page title
st.set_page_config(page_title="Kwin Stationers - The sky is a podium",
                   page_icon=":pencil2:",
                   layout="wide")

# Define a dictionary of articles
articles = {
    "article1": {
        "title":"Small Business",
        "author":"Winnie",
        "date":"March 11, 2023",
        "content":"Starting a small business can be a daunting task, but with the right tips and strategies, it can be a fulfilling and rewarding experience. One of the benefits of owning a small business is the flexibility and control it provides, allowing entrepreneurs to pursue their passions and create a work-life balance that suits their lifestyle. However, small business owners face several challenges, such as limited resources, fierce competition, and market saturation. Overcoming these challenges requires resilience, creativity, and a willingness to learn and adapt to changing market conditions. Effective marketing and promotion strategies are crucial to the success of any small business, and leveraging technology can help reach a broader audience and increase efficiency in operations. By staying informed, seeking mentorship, and embracing innovation, small business owners can position themselves for growth and success in their respective industries.",
    },
    "article2": {
        "title":"Growing a Business",
        "author":"Winnie",
        "date":"March 13, 2023",
        "content":"Growing a business requires intentional strategies and continuous innovation. One strategy for scaling a business is to focus on creating processes and systems that can be replicated as the business expands. Another important aspect of growth is fostering a culture of innovation to stay ahead of the competition. Hiring and managing employees who are aligned with the business's vision and values is also crucial to support growth. Expanding into new markets can also be a key driver of growth, but requires careful planning and research. Additionally, partnerships and collaborations with other businesses can provide opportunities for increased exposure and market penetration. By implementing these strategies and focusing on innovation, businesses can position themselves for sustained growth and success."
       
    },
    "article3": {
        "title":"Key Factors to Note in Business Growth:",
        "author":"Winnie",
        "date":"March 15, 2023",
        "content":"When it comes to business growth, there are several key factors that every entrepreneur should keep in mind. First and foremost, having a clear vision and mission for your business is essential. This will guide your decision-making processes and help you stay focused on your long-term goals. Additionally, developing a solid business plan that outlines your strategy, target market, and financial projections is crucial. Listening to customer feedback and continually improving your products or services can help you stay competitive and maintain customer loyalty. As an entrepreneur, it's also important to continuously learn and develop new skills to stay ahead of the curve. Lastly, having sound financial management practices in place is essential for sustainable business growth."
   
    },

    "article4": {
        "title":"Acquiring Funding",
        "author":"Winnie",
        "date":"March 17, 2023",
        "content":"Acquiring funding is often a crucial step in starting or growing a business. There are several types of funding available for small businesses, including loans from banks and other financial institutions, angel investing, venture capital, and crowdfunding. When preparing a pitch for investors, it's important to have a clear and concise message that highlights the unique value proposition of your business. Networking and building relationships with investors can also increase your chances of securing funding. In addition to traditional funding sources, crowdfunding has become an increasingly popular way to raise capital and validate new business ideas. By leveraging these funding sources and effectively communicating your business's value proposition, you can position your business for success."
    },
}
# Display articles sorted by date in descending order
sorted_articles = sorted(articles.values(), key=lambda x: x['date'], reverse=True)

# Display articles in streamlit
for article in sorted_articles:
    st.write(f"# {article['title']}")
    st.write(f"Author: {article['author']} | Date: {article['date']}")
    st.write(f"<div style='text-align: justify'>{article['content']}</div>", unsafe_allow_html=True)
    st.write('---')

# Add page footer
st.markdown("---")
st.write("© 2023 Kwin Stationers")

