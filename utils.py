
def justification_markdown(justification_data):
    found_dataset = False
    for dataset in justification_data:
        if dataset['is_relevant']:
            if not found_dataset:
                st.markdown("""
                            Below are the NDP datasets that are semantically closest to your request. 
                            Our searches and justifications are performed using AI. 
                            If you need more relevant datasets, please use other search tools on NDP.
                            """)
                found_dataset = True

            with st.container():
                st.markdown(f"""
                   <hr style="margin: 5px 0px 15px 0px; padding: 0px;" />
                   <table style="border: none; margin-bottom: 5pt;">
                      <tr style="border: none;">
                          <td style="vertical-align: top; border: none; font-weight: bold; margin: 0px; padding: 0px 8px;">
                               Dataset ID:
                          </td>
                          <td style="vertical-align: top; border: none;  margin: 0px 5px; padding: 0px;">
                               {dataset['dataset_id']}
                          </td>
                      </tr>
                      <tr style="border: none;">
                          <td style="vertical-align: top; border: none; font-weight: bold; margin: 0px; padding: 0px 8px;">
                               Title:
                          </td>
                          <td style="vertical-align: top; border: none;  margin: 0px; margin: 0px 5px; padding: 0px;">
                               {dataset['title']}
                           </td>
                      </tr>
                      <tr style="border: none;">
                          <td style="vertical-align: top; border: none; font-weight: bold; margin: 0px; padding: 0px 8px;">
                               Summary:
                           </td>
                          <td style="vertical-align: top; border: none; margin: 0px 5px; padding: 0px;">
                               {dataset['summary']}
                          </td>
                      </tr>
                      <tr style="border: none;">
                          <td style="vertical-align: top; border: none; font-weight: bold; margin: 0px; padding: 0px 8px;">
                               Justification:
                           </td>
                          <td style="vertical-align: top; border: none; margin: 0px 5px; padding: 0px;">
                               {dataset['reason']}
                          </td>
                      </tr>
                   </table>
                """, unsafe_allow_html=True)

    if not found_dataset:
        st.markdown(f"""
                    We couldn't locate a dataset closely aligned with your request. 
                    You can try refining your search for further attempts.
                    """)
    return ""