
import streamlit as st

def justification_markdown(justification_data):
    found_dataset = False
    for dataset in justification_data:
        if dataset['is_relevant']:
            if not found_dataset:
                st.markdown("""
                            Here are the datasets that are semantically closest to your query. If these datasets 
                            do not fully satisfy your requirements, you can refine or rephrase your query and 
                            try again.
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
