import React from 'react';
import { parseISO, toDate, intervalToDuration, formatDuration } from 'date-fns';
//import { toDate, format } from 'date-fns-tz';
import { Link } from 'react-router-dom';
import { Segment, Grid, Icon } from 'semantic-ui-react';
import Avatar from './Avatar';
import './style.css';

const BaseThread = ({ thread, topic }) => {
  const {
    thread_id,
    thread_name,
    pinned,
    thread_creator_name,
    thread_created_at,
    thread_creator_avatar,
    //naturaltime,
    post_count,
    last_activity,
  } = thread;
  const { topic_id } = topic;
  const thread_name_corrected =
    thread_name.length > 57
      ? thread_name.substring(0, 55) + '...'
      : thread_name;

  /*
  console.log(
    format(toDate(last_activity.post_created_at)),
    'yyyy/MM/dd kk:mm:ss'
  );
*/
  const post_date_humanized = last_activity.post_created_at
    ? formatDuration(
        intervalToDuration({
          start: toDate(parseISO(last_activity.post_created_at)),
          end: Date.now(),
        }),
        { format: ['years', 'months', 'days', 'hours', 'minutes'] }
      )
    : '';

  const thread_date_humanized = formatDuration(
    intervalToDuration({
      start: toDate(parseISO(thread_created_at)),
      end: Date.now(),
    }),
    { format: ['years', 'months', 'days', 'hours', 'minutes'] }
  );

  //let lastActivity = last_activity ? (
  let lastActivity = last_activity.post_id ? (
    <div className="forum-row">
      <Avatar
        className="forum-avatar"
        avatar={last_activity.post_creator_avatar}
        centered={false}
        link={`/user/${last_activity.post_creator_name}`}
      />
      <div className="forum-column">
        <div className="forum-name">{last_activity.post_creator_name}</div>
        <div className="forum-meta">
          <Link to={`/user/${last_activity.post_creator_name}`}>
            <Icon name="user" />
            {last_activity.post_creator_name}
          </Link>
          <b> - {post_date_humanized} ago</b>
        </div>
      </div>
    </div>
  ) : (
    <div className="forum-text forum-vertical">{'—  No activity —'}</div>
  );

  return (
    <Segment vertical key={thread_id}>
      <Grid textAlign="left" padded="horizontally">
        <Grid.Column width={7}>
          <Grid.Row>
            <div className="forum-row">
              <Avatar
                className="forum-avatar"
                avatar={thread_creator_avatar}
                centered={false}
                link={`/user/${thread_creator_name}`}
              />
              <div className="forum-column">
                <div>
                  <Icon name={pinned ? 'pin' : 'comment alternate outline'} />
                  <Link to={`/forum/${topic_id}/threads/${thread_id}`}>
                    {thread_name_corrected}
                  </Link>
                </div>
                <div className="forum-meta">
                  <Link to={`/user/${thread_creator_name}`}>
                    <Icon name="user" />
                    {thread_creator_name}
                  </Link>
                  <b> - {thread_date_humanized} ago</b>
                </div>
              </div>
            </div>
          </Grid.Row>
        </Grid.Column>
        <Grid.Column width={3}>
          <div className="forum-column forum-stats forum-vertical">
            <div style={{ paddingBottom: '5px' }}>
              <Icon name="comment outline" />
              {post_count}
              {post_count > 1 ? ' replies' : ' reply'}
            </div>
          </div>
        </Grid.Column>
        <Grid.Column width={6}>{lastActivity}</Grid.Column>
      </Grid>
    </Segment>
  );
};

export default BaseThread;
